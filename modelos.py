from __future__ import annotations

import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from metricas import aic_de, calcular

warnings.filterwarnings("ignore")

# Ventana reciente para estimar. La muestra de test no se toca:
# el pronóstico sale del último dato de entrenamiento, con menos historia.
TOPES_ENTRENAMIENTO = {
    "diaria": 260,
    "semanal": 104,
    "mensual": 120,
    "trimestral": 48,
    "anual": 40,
}


@dataclass
class Ajuste:
    nombre: str
    forecast: pd.Series | None = None
    fitted: pd.Series | None = None
    aic: float = field(default=np.nan)
    ok: bool = False
    nota: str = ""


def recortar_para_estimar(train: pd.Series, frecuencia: str) -> tuple[pd.Series, bool]:
    tope = TOPES_ENTRENAMIENTO.get(frecuencia, 168)
    if len(train) > tope:
        return train.iloc[-tope:], True
    return train, False


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
        # Semanal con ciclo 52: Holt-Winters se vuelve muy pesado.
        periodo = int(kw.get("seasonal_periods") or 0)
        if kw.get("seasonal") and periodo >= 52:
            return Ajuste(
                nombre,
                nota="En series semanales el ciclo anual se deja a ARIMA/Prophet; HW con 52 estaciones se atasca.",
            )
        model = ExponentialSmoothing(
            train.astype(float),
            initialization_method="heuristic",
            **kw,
        )
        fit = model.fit(optimized=True, method="L-BFGS-B")
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
        from statsmodels.tsa.arima.model import ARIMA

        y = train.astype(float)
        fit = None
        for orden in ((1, 1, 1), (0, 1, 1), (1, 0, 0)):
            try:
                fit = ARIMA(y, order=orden).fit()
                break
            except Exception:
                continue
        if fit is None:
            return Ajuste(nombre, nota="No se pudo ajustar un ARIMA parsimonioso.")
        fc = pd.Series(np.asarray(fit.forecast(h)).ravel(), index=_idx_futuro(train, h), name=nombre)
        fitted = pd.Series(np.asarray(fit.fittedvalues).ravel(), index=train.index[: len(fit.fittedvalues)], name=nombre)
        return Ajuste(nombre, fc, fitted, aic_de(fit), True)
    except Exception as exc:
        return Ajuste(nombre, nota=str(exc)[:160])


def prophet(train, h, periodo=12, frecuencia="mensual", **_):
    """Tendencia + Fourier estacional por mínimos cuadrados: la misma idea, sin Stan."""
    nombre = "Prophet"
    if len(train) < 16:
        return Ajuste(nombre, nota="Se necesitan al menos 16 observaciones.")
    try:
        y = train.astype(float).to_numpy()
        n = len(y)
        t = np.arange(n, dtype=float)
        piezas = [np.ones(n), t]
        per = int(periodo) if periodo and periodo >= 4 else 0
        if frecuencia == "diaria":
            per = 7
        armonicos = 2 if per >= 4 and n >= 2 * per else 0
        if armonicos:
            w = 2.0 * np.pi / per
            for j in range(1, armonicos + 1):
                piezas.append(np.sin(w * j * t))
                piezas.append(np.cos(w * j * t))
        X = np.column_stack(piezas)
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        fitted_vals = X @ coef
        t_f = np.arange(n, n + h, dtype=float)
        piezas_f = [np.ones(h), t_f]
        if armonicos:
            w = 2.0 * np.pi / per
            for j in range(1, armonicos + 1):
                piezas_f.append(np.sin(w * j * t_f))
                piezas_f.append(np.cos(w * j * t_f))
        fc_vals = np.column_stack(piezas_f) @ coef
        fc = pd.Series(fc_vals, index=_idx_futuro(train, h), name=nombre)
        fitted = pd.Series(fitted_vals, index=train.index, name=nombre)
        return Ajuste(nombre, fc, fitted, np.nan, True, "AIC no aplica.")
    except Exception as exc:
        return Ajuste(nombre, nota=str(exc)[:160])


def _lags_ml(y: np.ndarray, lags: int):
    ventanas = np.lib.stride_tricks.sliding_window_view(y, lags + 1)
    return ventanas[:, :-1].copy(), ventanas[:, -1].copy()


def _ml(nombre, modelo, train, h, periodo=12):
    y = train.astype(float).to_numpy()
    lags = int(max(3, min(periodo if periodo and periodo > 1 else 6, 8, max(3, len(y) // 4))))
    if len(y) < lags + 8:
        return Ajuste(nombre, nota="Historia corta para un modelo de rezagos.")
    try:
        X, t = _lags_ml(y, lags)
        modelo.fit(X, t)
        fitted_vals = modelo.predict(X)
        fitted = pd.Series(fitted_vals, index=train.index[lags : lags + len(fitted_vals)], name=nombre)
        hist = y.tolist()
        preds = []
        for _ in range(h):
            x = np.asarray(hist[-lags:], dtype=float).reshape(1, -1)
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
        from sklearn.svm import LinearSVR
    except ModuleNotFoundError:
        return Ajuste("SVR", nota="Falta scikit-learn. Instale con: pip install scikit-learn")

    try:
        nucleo = LinearSVR(C=1.0, epsilon=0.05, max_iter=1500, dual="auto")
    except TypeError:
        nucleo = LinearSVR(C=1.0, epsilon=0.05, max_iter=1500)
    m = make_pipeline(StandardScaler(), nucleo)
    return _ml("SVR", m, train, h, periodo)


def rf(train, h, periodo=12, **_):
    try:
        from sklearn.ensemble import RandomForestRegressor
    except ModuleNotFoundError:
        return Ajuste("RF", nota="Falta scikit-learn. Instale con: pip install scikit-learn")

    m = RandomForestRegressor(
        n_estimators=20,
        max_depth=5,
        min_samples_leaf=2,
        random_state=7,
        n_jobs=1,
    )
    return _ml("RF", m, train, h, periodo)


def xgb(train, h, periodo=12, **_):
    try:
        from xgboost import XGBRegressor
    except ModuleNotFoundError:
        return Ajuste("XGBoost", nota="Falta el paquete xgboost. Instale con: pip install xgboost")

    m = XGBRegressor(
        n_estimators=20,
        max_depth=3,
        learning_rate=0.12,
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


def ajustar_todos(
    train: pd.Series, h: int, periodo: int, frecuencia: str, progreso=None
) -> tuple[dict[str, Ajuste], pd.Series, bool]:
    train_uso, recortada = recortar_para_estimar(train, frecuencia)
    out = {}
    n = len(CATALOGO_MODELOS)
    for i, (nombre, fn) in enumerate(CATALOGO_MODELOS, start=1):
        if progreso is not None:
            progreso.progress(i / n, text=f"Estimando {nombre}…")
        out[nombre] = fn(train_uso, h, periodo=periodo, frecuencia=frecuencia)
    if progreso is not None:
        progreso.progress(1.0, text="Listo")
    return out, train_uso, recortada


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
