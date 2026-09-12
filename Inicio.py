import streamlit as st

from ui import aplicar, hero, tarjeta

st.set_page_config(
    page_title="Mesa de pronóstico",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar()

hero(
    "Analítica Financiera  ·  Pontificia Universidad Javeriana",
    "Mesa de pronóstico",
    "Compare modelos sobre series reales y lleve a la mesa el que mejor rinde en la muestra de test.",
)

c1, c2, c3 = st.columns(3)
with c1:
    tarjeta("1. Los modelos", "Qué hace cada especificación y cuándo tiene sentido usarla.")
with c2:
    tarjeta("2. La serie", "Elija una base, lea el contexto y grafique la variable.")
with c3:
    tarjeta("3. La decisión", "Compare RMSE, MAE, MAPE, MASE y AIC en la muestra de entrenamiento y en la de test.")

st.markdown("")
st.markdown(
    """
Las bases ya están cargadas. No hay que subir archivos.

La pregunta de la aplicación no es “¿cuál modelo es más elegante?”.
Es **cuál comete menos error en la muestra de test** — el mismo criterio
que usaría Dirección Financiera para un cupo, una meta o una compra de inventario.
"""
)

if st.session_state.get("serie") is not None:
    s = st.session_state["serie"]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Serie en mesa", st.session_state.get("rotulo", "—"))
    m2.metric("Observaciones", f"{len(s):,}")
    m3.metric("Inicio", s.index.min().strftime("%Y-%m"))
    m4.metric("Fin", s.index.max().strftime("%Y-%m"))
    st.success("Hay una serie lista. Siga a **La serie** para revisarla o a **La decisión** para estimar.")
else:
    st.info("Empiece por **La serie** (menú izquierdo): elija base, entidad si aplica, y una variable.")
