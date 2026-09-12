import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from datos import serie_para_plot
from modelos import recomendar, tabla_errores
from servidor import clave_estimacion, estimar_compartido
from ui import aplicar, hero, reco

st.set_page_config(page_title="La decisión", page_icon="◈", layout="wide")
aplicar()

hero(
    "Muestra de entrenamiento y muestra de test",
    "La decisión",
    "Los diez modelos se estiman con la muestra de entrenamiento y se comparan en la muestra de test. Gana quien falla menos en test. Si varios eligen la misma serie y la misma ventana, el servidor reutiliza el cálculo.",
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
    clave = clave_estimacion(
        st.session_state.get("dataset_id"),
        st.session_state.get("filtros"),
        st.session_state.get("medida"),
        h,
    )
    barra = st.progress(0.0, text="Preparando…")
    with st.spinner(
        "Si hay más personas estimando, espera su turno: el servidor hace un cálculo a la vez "
        "para no saturarse. Si esa serie ya se pidió, el resultado sale al instante."
    ):
        ajustes, train_est, recortada, de_cache = estimar_compartido(
            clave, train, h, periodo, frecuencia, progreso=barra
        )
    barra.progress(1.0, text="Listo (ya estaba en el servidor)" if de_cache else "Listo")
    st.session_state["ajustes"] = ajustes
    st.session_state["train"] = train
    st.session_state["train_est"] = train_est
    st.session_state["recorte_est"] = recortada
    st.session_state["test"] = test
    st.session_state["h_usado"] = h
    st.session_state["de_cache"] = de_cache

ajustes = st.session_state.get("ajustes")
if not ajustes:
    st.info(
        "Pulse el botón para estimar. En series largas se usa una ventana reciente de la "
        "muestra de entrenamiento para que ARIMA, Prophet y los modelos de rezagos no se atasquen."
    )
    st.stop()

train = st.session_state["train"]
train_est = st.session_state.get("train_est", train)
test = st.session_state["test"]
if st.session_state.get("de_cache"):
    st.caption("Este resultado ya estaba en el servidor: otra sesión pidió la misma serie y la misma ventana.")
if st.session_state.get("recorte_est"):
    st.caption(
        f"Para estimar se usaron los últimos {len(train_est):,} periodos de la muestra de "
        f"entrenamiento ({train_est.index.min():%Y-%m} → {train_est.index.max():%Y-%m}). "
        "El gráfico muestra la serie completa; las métricas de entrenamiento son de esa ventana."
    )
df = tabla_errores(ajustes, train_est, test)
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
        st.plotly_chart(figb, use_container_width=True, config={"displayModeBar": False})

with tabs[1]:
    fig = go.Figure()
    train_vista = serie_para_plot(train)
    fig.add_trace(
        go.Scatter(
            x=train_vista.index,
            y=train_vista.values,
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
        yaxis=dict(
            gridcolor="#efe6d4",
            title=st.session_state.get("medida_nombre") or st.session_state.get("medida", "Valor"),
        ),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

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
