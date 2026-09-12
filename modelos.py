from __future__ import annotations

import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from metricas import aic_de, calcular

warnings.filterwarnings("ignore")


@dataclass
class Ajuste:
    nombre: str
    forecast: pd.Series | None = None
    fitted: pd.Series | None = None
    aic: float = field(default=np.nan)
    ok: bool = False
    nota: str = ""


def _idx_futuro(train: pd.Series, h: int) -> pd.DatetimeIndex:
    freq = pd.infer_freq(train.index)
    if freq:
        return pd.date_range(train.index[-1], periods=h + 1, freq=freq)[1:]
    delta = train.index[-1] - train.index[-2]
    return pd.DatetimeIndex([train.index[-1] + (i + 1) * delta for i in range(h)])


def _ets(train, h, **kw) -> Ajuste:
    nombre = kw.pop("nombre")
    try:
        if kw.get("seasonal") and (kw.get("seasonal_periods") or 0) < 2:
            return Ajuste(nombre, nota="La frecuencia no admite estacionalidad.")
        if kw.get("seasonal") == "mul" and (train <= 0).any():
            return Ajuste(nombre, nota="Requiere valores estrictamente positivos.")
        if kw.get("seasonal") and len(train) < 2 * int(kw.get("seasonal_periods") or 12):
            return Ajuste(nombre, nota="Historia insuficiente para un ciclo estacional.")
        model = ExponentialSmoothing(train.astype(float), **kw)
        fit = model.fit(optimized=True)
        fc = pd.Series(np.asarray(fit.forecast(h)).ravel(), index=_idx_futuro(train, h), name=nombre)
        fitted = pd.Series(np.asarray(fit.fittedvalues).ravel(), index=train.index[: len(fit.fittedvalues)], name=nombre)
        return Ajuste(nombre, fc, fitted, aic_de(fit), True)
    except Exception as exc:
        return Ajuste(nombre, nota=str(exc)[:160])


def ses(train, h, **_):
    return _ets(train, h, nombre="SES", trend=None, seasonal=None)


def holt(train, h, **_):
    return _ets(train, h, nombre="Holt", trend="add", seasonal=None)


def holt_amort(train, h, **_):
    return _ets(train, h, nombre="Holt amortiguado", trend="add", damped_trend=True, seasonal=None)


def hw_add(train, h, periodo=12, **_):
    return _ets(train, h, nombre="HW aditivo", trend="add", seasonal="add", seasonal_periods=periodo)


def hw_mult(train, h, periodo=12, **_):
    return _ets(train, h, nombre="HW multiplicativo", trend="add", seasonal="mul", seasonal_periods=periodo)


def arima(train, h, periodo=12, **_):
    nombre = "ARIMA"
    try:
        from pmdarima import auto_arima

        estacional = bool(periodo and periodo >= 4 and len(train) >= 3 * periodo)
        fit = auto_arima(
            train.astype(float),
            seasonal=estacional,
            m=int(periodo) if estacional else 1,
            stepwise=True,
            approximation=True,
            suppress_warnings=True,
            error_action="ignore",
        )
        fc = pd.Series(np.asarray(fit.predict(h)).ravel(), index=_idx_futuro(train, h), name=nombre)
        fitted = pd.Series(np.asarray(fit.predict_in_sample()).ravel(), index=train.index[: len(train)], name=nombre)
        return Ajuste(nombre, fc, fitted, aic_de(fit), True)
    except Exception as exc:
        return Ajuste(nombre, nota=str(exc)[:160])


def prophet(train, h, periodo=12, frecuencia="mensual", **_):
    nombre = "Prophet"
    if len(train) < 20:
        return Ajuste(nombre, nota="Se necesitan al menos 20 observaciones.")
    try:
        import logging

        from prophet import Prophet

        logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
        logging.getLogger("prophet").setLevel(logging.WARNING)

        df = pd.DataFrame({"ds": pd.to_datetime(train.index), "y": train.astype(float).values})
        yearly = frecuencia in ("mensual", "trimestral", "semanal", "diaria") and len(train) >= 24
        weekly = frecuencia == "diaria"
        m = Prophet(
            yearly_seasonality=yearly,
            weekly_seasonality=weekly,
            daily_seasonality=False,
            seasonality_mode="additive",
        )
        m.fit(df)
        futuro = pd.DataFrame({"ds": _idx_futuro(train, h)})
        pred_fc = m.predict(futuro)
        pred_in = m.predict(df)
        fc = pd.Series(pred_fc["yhat"].to_numpy(), index=_idx_futuro(train, h), name=nombre)
        fitted = pd.Series(pred_in["yhat"].to_numpy(), index=train.index, name=nombre)
        return Ajuste(nombre, fc, fitted, np.nan, True, "AIC no aplica.")
    except Exception as exc:
        return Ajuste(nombre, nota=str(exc)[:160])


def _lags_ml(y: np.ndarray, lags: int):
    X, t = [], []
    for i in range(lags, len(y)):
        X.append(y[i - lags : i])
        t.append(y[i])
    return np.asarray(X), np.asarray(t)


def _ml(nombre, modelo, train, h, periodo=12):
    y = train.astype(float).to_numpy()
    lags = int(max(3, min(periodo if periodo and periodo > 1 else 6, 12, max(3, len(y) // 4))))
    if len(y) < lags + 8:
        return Ajuste(nombre, nota="Historia corta para un modelo de rezagos.")
    try:
        X, t = _lags_ml(y, lags)
        modelo.fit(X, t)
        fitted_vals = modelo.predict(X)
        fitted = pd.Series(fitted_vals, index=train.index[lags : lags + len(fitted_vals)], name=nombre)
        hist = list(y)
        preds = []
        for _ in range(h):
            x = np.asarray(hist[-lags:]).reshape(1, -1)
            preds.append(float(modelo.predict(x)[0]))
            hist.append(preds[-1])
        fc = pd.Series(preds, index=_idx_futuro(train, h), name=nombre)
        return Ajuste(nombre, fc, fitted, np.nan, True, "AIC no aplica.")
    except Exception as exc:
        return Ajuste(nombre, nota=str(exc)[:160])


def svr(train, h, periodo=12, **_):
    try:
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.svm import SVR
    except ModuleNotFoundError:
        return Ajuste("SVR", nota="Falta scikit-learn. Instale con: pip install scikit-learn")

    m = make_pipeline(StandardScaler(), SVR(C=10.0, epsilon=0.05, kernel="rbf"))
    return _ml("SVR", m, train, h, periodo)


def rf(train, h, periodo=12, **_):
    try:
        from sklearn.ensemble import RandomForestRegressor
    except ModuleNotFoundError:
        return Ajuste("RF", nota="Falta scikit-learn. Instale con: pip install scikit-learn")

    m = RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=7)
    return _ml("RF", m, train, h, periodo)


def xgb(train, h, periodo=12, **_):
    try:
        from xgboost import XGBRegressor
    except ModuleNotFoundError:
        return Ajuste("XGBoost", nota="Falta el paquete xgboost. Instale con: pip install xgboost")

    m = XGBRegressor(
        n_estimators=250,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        n_jobs=1,
        verbosity=0,
    )
    return _ml("XGBoost", m, train, h, periodo)


CATALOGO_MODELOS = [
    ("SES", ses),
    ("Holt", holt),
    ("Holt amortiguado", holt_amort),
    ("HW aditivo", hw_add),
    ("HW multiplicativo", hw_mult),
    ("ARIMA", arima),
    ("Prophet", prophet),
    ("SVR", svr),
    ("RF", rf),
    ("XGBoost", xgb),
]


def ajustar_todos(train: pd.Series, h: int, periodo: int, frecuencia: str, progreso=None) -> dict[str, Ajuste]:
    out = {}
    n = len(CATALOGO_MODELOS)
    for i, (nombre, fn) in enumerate(CATALOGO_MODELOS, start=1):
        if progreso is not None:
            progreso.progress(i / n, text=f"Estimando {nombre}…")
        out[nombre] = fn(train, h, periodo=periodo, frecuencia=frecuencia)
    if progreso is not None:
        progreso.progress(1.0, text="Listo")
    return out


def tabla_errores(ajustes: dict[str, Ajuste], train: pd.Series, test: pd.Series) -> pd.DataFrame:
    filas = []
    for nombre, aj in ajustes.items():
        fila = {"Modelo": nombre, "Estado": "OK" if aj.ok else aj.nota or "No estimado"}
        if aj.ok and aj.forecast is not None:
            te = calcular(test, aj.forecast, train)
            tr = calcular(train, aj.fitted, train) if aj.fitted is not None else {k: np.nan for k in te}
            fila.update(
                {
                    "RMSE entrenamiento": tr["RMSE"],
                    "MAE entrenamiento": tr["MAE"],
                    "MAPE entrenamiento": tr["MAPE"],
                    "MASE entrenamiento": tr["MASE"],
                    "RMSE test": te["RMSE"],
                    "MAE test": te["MAE"],
                    "MAPE test": te["MAPE"],
                    "MASE test": te["MASE"],
                    "AIC": aj.aic,
                }
            )
        filas.append(fila)
    return pd.DataFrame(filas)


def recomendar(df: pd.DataFrame) -> dict:
    ok = df.dropna(subset=["RMSE test"]) if "RMSE test" in df.columns else df.iloc[0:0]
    if ok.empty:
        return {"modelo": None, "texto": "Ningún modelo produjo un pronóstico utilizable en la muestra de test."}
    mejor = ok.loc[ok["RMSE test"].idxmin()]
    coinciden = []
    for col in ("MAE test", "MAPE test", "MASE test"):
        if col in ok and ok[col].notna().any():
            if ok.loc[ok[col].idxmin(), "Modelo"] == mejor["Modelo"]:
                coinciden.append(col.replace(" test", ""))
    aic_txt = ""
    if "AIC" in ok and ok["AIC"].notna().any():
        gan_aic = ok.loc[ok["AIC"].idxmin(), "Modelo"]
        if gan_aic == mejor["Modelo"]:
            aic_txt = " El AIC en la muestra de entrenamiento apunta en la misma dirección."
        else:
            aic_txt = (
                f" El menor AIC en la muestra de entrenamiento es {gan_aic}; el AIC no reemplaza "
                "el error en la muestra de test cuando el objetivo es pronosticar."
            )
    extra = (
        f" MAE, MAPE y MASE en la muestra de test también eligen a {mejor['Modelo']}."
        if len(coinciden) == 3
        else (
            f" En la muestra de test coinciden: {', '.join(coinciden)}."
            if coinciden
            else " Las demás métricas en la muestra de test no coinciden del todo."
        )
    )
    texto = (
        f"Para esta serie, la evidencia en la muestra de test (menor RMSE) corresponde a "
        f"**{mejor['Modelo']}**. RMSE test = {mejor['RMSE test']:.4f}.{extra}{aic_txt} "
        "Ese es el modelo de trabajo que convendría llevar a la mesa de presupuesto, "
        "salvo que un criterio de negocio (interpretabilidad, signo de los valores, estacionalidad) "
        "justifique otro."
    )
    return {"modelo": mejor["Modelo"], "rmse": float(mejor["RMSE test"]), "texto": texto}
