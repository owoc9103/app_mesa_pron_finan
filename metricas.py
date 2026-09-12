from __future__ import annotations

import numpy as np
import pandas as pd


def _alinear(real: pd.Series, pred: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    s = pd.concat({"r": real, "p": pred}, axis=1).dropna()
    return s["r"].to_numpy(dtype=float), s["p"].to_numpy(dtype=float)


def calcular(real: pd.Series, pred: pd.Series, train: pd.Series | None = None) -> dict:
    y, yhat = _alinear(real, pred)
    if len(y) == 0:
        return {k: np.nan for k in ("RMSE", "MAE", "MAPE", "MASE")}
    rmse = float(np.sqrt(np.mean((y - yhat) ** 2)))
    mae = float(np.mean(np.abs(y - yhat)))
    mask = y != 0
    mape = float(np.mean(np.abs((y[mask] - yhat[mask]) / y[mask])) * 100) if mask.any() else np.nan
    if train is not None and len(train.dropna()) > 1:
        mae_naive = float(np.mean(np.abs(np.diff(train.dropna().to_numpy(dtype=float)))))
        mase = mae / mae_naive if mae_naive > 0 else np.nan
    else:
        mase = np.nan
    return {"RMSE": rmse, "MAE": mae, "MAPE": mape, "MASE": mase}


def aic_de(fit) -> float:
    if fit is None:
        return np.nan
    for attr in ("aic", "aicc"):
        if hasattr(fit, attr):
            val = getattr(fit, attr)
            try:
                val = val() if callable(val) else val
                if val is not None and np.isfinite(float(val)):
                    return float(val)
            except (TypeError, ValueError):
                pass
    return np.nan
