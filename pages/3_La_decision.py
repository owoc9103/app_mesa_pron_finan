import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modelos import ajustar_todos, recomendar, tabla_errores
from ui import aplicar, hero, reco

st.set_page_config(page_title="La decisión", page_icon="◈", layout="wide")
aplicar()

hero(
    "Muestra de entrenamiento y muestra de test",
    "La decisión",
    "Los diez modelos se estiman con la muestra de entrenamiento y se comparan en la muestra de test. Gana quien falla menos en test.",
)

serie = st.session_state.get("serie")
if serie is None:
    st.warning("Todavía no hay una serie en la mesa. Vaya a **La serie** y elija base y variable.")
    st.stop()

meta = st.session_state.get("meta", {})
rotulo = st.session_state.get("rotulo", st.session_state.get("medida", "Serie"))
periodo = int(meta.get("periodo") or 12)
frecuencia = meta.get("frecuencia", "mensual")
h_sug = int(st.session_state.get("h_sugerido") or max(4, len(serie) // 5))
h_max = max(4, len(serie) // 3)

c0, c1 = st.columns((2, 1))
with c0:
    st.markdown(f"**En mesa:** {rotulo}")
    st.caption(f"{len(serie):,} observaciones  ·  {serie.index.min().date()} → {serie.index.max().date()}  ·  {frecuencia}")
with c1:
    h = st.slider("Periodos de la muestra de test", 3, int(h_max), min(h_sug, h_max))

train = serie.iloc[:-h]
test = serie.iloc[-h:]
t1, t2, t3 = st.columns(3)
t1.metric("Muestra de entrenamiento", f"{len(train):,}")
t2.metric("Muestra de test", f"{len(test):,}")
t3.metric("La muestra de test inicia", test.index.min().strftime("%Y-%m-%d"))

correr = st.button("Estimar los diez modelos y comparar", type="primary", use_container_width=True)

if correr:
    barra = st.progress(0.0, text="Preparando…")
    st.session_state["ajustes"] = ajustar_todos(train, h, periodo, frecuencia, progreso=barra)
    st.session_state["train"] = train
    st.session_state["test"] = test
    st.session_state["h_usado"] = h

ajustes = st.session_state.get("ajustes")
if not ajustes:
    st.info("Pulse el botón para estimar. Tardará un momento: ARIMA, Prophet y los modelos de rezagos pesan más.")
    st.stop()

train = st.session_state["train"]
test = st.session_state["test"]
df = tabla_errores(ajustes, train, test)
veredicto = recomendar(df)

if veredicto["modelo"]:
    reco(
        f"<strong>Modelo de trabajo:</strong> {veredicto['modelo']}<br/>"
        + veredicto["texto"].replace("**", "")
    )
else:
    st.error(veredicto["texto"])

tabs = st.tabs(["Métricas", "Pronósticos vs real", "Detalle"])

with tabs[0]:
    st.markdown(
        "Errores en la **muestra de entrenamiento** y en la **muestra de test**. "
        "El modelo de trabajo se elige por el error en la muestra de test."
    )
    mostrar = df.copy()
    num_cols = [c for c in mostrar.columns if c not in ("Modelo", "Estado")]
    for c in num_cols:
        mostrar[c] = pd.to_numeric(mostrar[c], errors="coerce")
    st.dataframe(
        mostrar.style.format(
            {c: "{:.3f}" for c in num_cols},
            na_rep="—",
        ).highlight_min(
            subset=[c for c in ("RMSE test", "MAE test", "MAPE test", "MASE test") if c in mostrar.columns],
            color="#e7f3e4",
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Descargar tabla de errores",
        data=mostrar.to_csv(index=False).encode("utf-8-sig"),
        file_name="comparacion_modelos.csv",
        mime="text/csv",
    )
    if "RMSE test" in df.columns and df["RMSE test"].notna().any():
        figb = go.Figure()
        ok = df.dropna(subset=["RMSE test"]).sort_values("RMSE test")
        colores = ["#c9a227" if m == veredicto["modelo"] else "#1b365d" for m in ok["Modelo"]]
        figb.add_trace(go.Bar(x=ok["Modelo"], y=ok["RMSE test"], marker_color=colores))
        figb.update_layout(
            height=360,
            title="RMSE en la muestra de test (menor es mejor)",
            paper_bgcolor="#F7F4EE",
            plot_bgcolor="#fffdf8",
            margin=dict(l=10, r=10, t=50, b=10),
            yaxis=dict(gridcolor="#efe6d4", title="RMSE"),
        )
        st.plotly_chart(figb, use_container_width=True)

with tabs[1]:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=train.index,
            y=train.values,
            name="Muestra de entrenamiento",
            line=dict(color="#8a8373", width=1.6),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=test.index,
            y=test.values,
            name="Real (muestra de test)",
            mode="lines+markers",
            line=dict(color="#111827", width=2.6),
            marker=dict(size=6),
        )
    )
    paleta = [
        "#1b365d",
        "#c9a227",
        "#0f766e",
        "#9f1239",
        "#4338ca",
        "#b45309",
        "#0369a1",
        "#4d7c0f",
        "#7c3aed",
        "#be185d",
    ]
    i = 0
    for nombre, aj in ajustes.items():
        if not aj.ok or aj.forecast is None:
            continue
        fig.add_trace(
            go.Scatter(
                x=aj.forecast.index,
                y=aj.forecast.values,
                name=nombre,
                line=dict(color=paleta[i % len(paleta)], width=1.7, dash="dash"),
            )
        )
        i += 1
    fig.add_vline(x=test.index.min(), line_dash="dot", line_color="#9a917c")
    fig.update_layout(
        height=520,
        hovermode="x unified",
        paper_bgcolor="#F7F4EE",
        plot_bgcolor="#fffdf8",
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(gridcolor="#efe6d4", title=st.session_state.get("medida", "Valor")),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)

    panel = pd.DataFrame({"fecha": test.index, "real": test.values})
    for nombre, aj in ajustes.items():
        if aj.ok and aj.forecast is not None:
            panel[nombre] = np.asarray(aj.forecast.reindex(test.index))
    st.dataframe(panel.round(4), use_container_width=True, hide_index=True)
    st.download_button(
        "Descargar reales y pronósticos de la muestra de test",
        data=panel.to_csv(index=False).encode("utf-8-sig"),
        file_name="pronosticos_vs_real.csv",
        mime="text/csv",
    )

with tabs[2]:
    fallidos = [f"**{n}:** {a.nota}" for n, a in ajustes.items() if not a.ok]
    if fallidos:
        st.markdown("Modelos que no se pudieron estimar en esta serie:")
        for f in fallidos:
            st.markdown(f"- {f}")
    else:
        st.caption("Los diez modelos devolvieron un pronóstico.")
    st.markdown(
        "Holt-Winters multiplicativo exige valores positivos. "
        "HW y ARIMA estacional piden historia de al menos un par de ciclos. "
        "Prophet, SVR, RF y XGBoost no tienen AIC; en esos casos la columna queda vacía."
    )
