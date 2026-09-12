from __future__ import annotations

import pandas as pd
import streamlit as st

from catalogo import CATALOGO, DATA_DIR, OCULTAR


@st.cache_data(show_spinner=False)
def cargar_tabla(dataset_id: str) -> pd.DataFrame:
    ruta = DATA_DIR / f"{dataset_id}.csv"
    meta = CATALOGO[dataset_id]
    header = pd.read_csv(ruta, nrows=0).columns.tolist()
    keep = {"fecha"}
    keep.update(meta.get("variables", {}))
    keep.update(meta.get("entidades", []))
    usecols = [c for c in header if c in keep]
    if not usecols:
        usecols = None
    kwargs = {"usecols": usecols, "parse_dates": ["fecha"]}
    try:
        df = pd.read_csv(ruta, engine="pyarrow", **kwargs)
    except Exception:
        df = pd.read_csv(ruta, **kwargs)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    return df.dropna(subset=["fecha"]).sort_values("fecha")


@st.cache_data(show_spinner=False)
def valores_unicos(dataset_id: str, col: str, filtros: tuple) -> list[str]:
    df = cargar_tabla(dataset_id)
    for clave, valor in filtros:
        if clave in df.columns:
            df = df[df[clave] == valor]
    return sorted(df[col].dropna().astype(str).unique().tolist())


def columnas_medida(df: pd.DataFrame, dataset_id: str) -> list[str]:
    meta = CATALOGO[dataset_id]
    declared = list(meta.get("variables", {}).keys())
    numericas = [
        c
        for c in df.columns
        if c != "fecha" and c not in OCULTAR and pd.api.types.is_numeric_dtype(df[c])
    ]
    orden = [c for c in declared if c in numericas]
    for c in numericas:
        if c not in orden:
            orden.append(c)
    return orden


def columnas_entidad(df: pd.DataFrame, dataset_id: str) -> list[str]:
    meta = CATALOGO[dataset_id]
    declaradas = [c for c in meta.get("entidades", []) if c in df.columns]
    if declaradas:
        return declaradas
    extra = []
    for c in df.columns:
        if c in ("fecha",) or c in OCULTAR:
            continue
        if not pd.api.types.is_numeric_dtype(df[c]):
            extra.append(c)
    return extra


def filtrar(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    out = df
    for col, val in filtros.items():
        if col in out.columns and val is not None:
            out = out[out[col] == val]
    return out


@st.cache_data(show_spinner=False)
def extraer_serie_cache(dataset_id: str, medida: str, filtros: tuple) -> pd.Series:
    df = cargar_tabla(dataset_id)
    for clave, valor in filtros:
        if clave in df.columns:
            df = df[df[clave] == valor]
    return extraer_serie(df, medida)


def serie_para_plot(serie: pd.Series, max_n: int = 360) -> pd.Series:
    if serie is None or len(serie) <= max_n:
        return serie
    return serie.iloc[:: max(1, len(serie) // max_n)]


def extraer_serie(df: pd.DataFrame, medida: str) -> pd.Series:
    g = df.groupby("fecha", as_index=True)[medida].mean().sort_index()
    g.name = medida
    freq = pd.infer_freq(g.index)
    if freq:
        g = g.asfreq(freq)
    return g.dropna()


def horizonte_sugerido(n: int, h_cat: int, periodo: int) -> int:
    tope = max(4, n // 4)
    if periodo and periodo >= 4:
        tope = min(tope, max(periodo, n - 2 * periodo))
    h = min(h_cat, tope, n - 8) if n > 16 else max(3, n // 5)
    return int(max(3, h))
