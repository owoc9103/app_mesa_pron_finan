import plotly.graph_objects as go
import streamlit as st

from catalogo import CATALOGO, etiqueta, ids_ordenados
from datos import (
    cargar_tabla,
    columnas_entidad,
    columnas_medida,
    extraer_serie,
    filtrar,
    horizonte_sugerido,
)
from ui import aplicar, hero

st.set_page_config(page_title="La serie", page_icon="◈", layout="wide")
aplicar()

hero(
    "Carga automática",
    "La serie",
    "Elija un tablero, lea qué está midiendo y deje una variable en la mesa.",
)

ids = ids_ordenados()
etiquetas = {i: etiqueta(i) for i in ids}
elegido = st.selectbox("Base de datos", ids, format_func=lambda i: etiquetas[i])
meta = CATALOGO[elegido]
df = cargar_tabla(elegido)

c1, c2 = st.columns((1.35, 1))
with c1:
    st.markdown(f"### {meta['titulo']}")
    st.markdown(meta["contexto"])
    st.caption(f"Frecuencia {meta['frecuencia']}")
with c2:
    st.metric("Filas", f"{len(df):,}")
    st.metric("Frecuencia", meta["frecuencia"])
    st.metric("Rango", f"{df['fecha'].min().strftime('%Y-%m')} → {df['fecha'].max().strftime('%Y-%m')}")

entidad_cols = columnas_entidad(df, elegido)
filtros = {}
if entidad_cols:
    st.markdown("#### Recorte de la base")
    st.caption("Esta tabla reúne varias series. Elija el corte que quiere poner en la mesa.")
    cols = st.columns(len(entidad_cols))
    trabajo = df
    for col, slot in zip(entidad_cols, cols):
        opciones = sorted(trabajo[col].dropna().astype(str).unique().tolist())
        sugeridas = meta.get("entidad_sugerida", {})
        default = sugeridas.get(col)
        idx = opciones.index(default) if default in opciones else 0
        val = slot.selectbox(col, opciones, index=idx)
        filtros[col] = val
        trabajo = trabajo[trabajo[col] == val]
else:
    trabajo = df

medidas = columnas_medida(trabajo, elegido)
if not medidas:
    st.error("No hay una variable numérica en este recorte.")
    st.stop()

sugerida = meta.get("sugerida")
idx_m = medidas.index(sugerida) if sugerida in medidas else 0
medida = st.selectbox("Variable a pronosticar", medidas, index=idx_m)
st.info(meta.get("variables", {}).get(medida, "Variable numérica de la base."))

serie = extraer_serie(trabajo, medida)
if len(serie) < 16:
    st.warning("Quedan pocas observaciones. El recorte puede ser demasiado estrecho.")

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=serie.index,
        y=serie.values,
        mode="lines",
        name=medida,
        line=dict(color="#1b365d", width=2.2),
    )
)
fig.update_layout(
    height=420,
    margin=dict(l=10, r=10, t=40, b=10),
    title=dict(text=f"{medida}", font=dict(family="Fraunces, serif", size=18, color="#1b365d")),
    xaxis_title="Tiempo",
    yaxis_title=medida,
    paper_bgcolor="#F7F4EE",
    plot_bgcolor="#fffdf8",
    hovermode="x unified",
    xaxis=dict(rangeslider=dict(visible=True), showgrid=False),
    yaxis=dict(gridcolor="#efe6d4"),
)
st.plotly_chart(fig, use_container_width=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Observaciones", f"{len(serie):,}")
k2.metric("Media", f"{serie.mean():,.2f}")
k3.metric("Mínimo", f"{serie.min():,.2f}")
k4.metric("Máximo", f"{serie.max():,.2f}")

rotulo_ent = " · ".join(f"{k}: {v}" for k, v in filtros.items())
rotulo = f"{meta['titulo']} — {medida}" + (f" ({rotulo_ent})" if rotulo_ent else "")

if st.button("Poner esta serie en la mesa", type="primary", use_container_width=True):
    st.session_state["serie"] = serie
    st.session_state["dataset_id"] = elegido
    st.session_state["medida"] = medida
    st.session_state["filtros"] = filtros
    st.session_state["meta"] = meta
    st.session_state["rotulo"] = rotulo
    st.session_state["h_sugerido"] = horizonte_sugerido(len(serie), meta["h"], meta["periodo"])
    st.session_state.pop("ajustes", None)
    st.success(f"Quedó en mesa: {rotulo}. Siga a **La decisión**.")
