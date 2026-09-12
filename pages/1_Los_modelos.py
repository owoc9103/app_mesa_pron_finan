import streamlit as st
from ui import aplicar, hero

st.set_page_config(page_title="Los modelos", page_icon="◈", layout="wide")
aplicar()

hero(
    "Biblioteca de especificaciones",
    "Los modelos",
    "Diez formas de proyectar una sola variable. La app las estima todas; aquí está qué está haciendo cada una.",
)

st.markdown(
    "Ningún modelo es universal. SES sostiene un nivel; Holt sigue una tendencia; "
    "Holt-Winters añade temporada; ARIMA y Prophet son más flexibles; "
    "SVR, bosques y XGBoost aprenden rezagos sin imponer una forma de suavizado."
)

bloques = [
    (
        "SES — suavizado exponencial simple",
        """
Asigna más peso a lo reciente y menos a lo antiguo. Un solo parámetro de nivel.

**Sirve cuando** la serie oscila alrededor de un nivel, sin tendencia clara ni temporada.

**Riesgo:** si hay crecimiento o picos de calendario, se queda corto y aplana el presupuesto.
""",
    ),
    (
        "Holt — tendencia",
        """
Extiende SES con una pendiente. El pronóstico avanza el nivel más *h* veces la tendencia.

**Sirve cuando** hay crecimiento o caída persistente y no hay un patrón que se repita cada año.

**Riesgo:** proyecta la pendiente para siempre; en series que se frenan, sobreestima.
""",
    ),
    (
        "Holt amortiguado",
        """
Como Holt, pero la tendencia se va apagando. El crecimiento no se extrapola en línea recta.

**Sirve cuando** hubo expansión y luego madurez: utilidad que crece y se aplana, mercados que saturan.

**Riesgo:** si la pendiente sigue viva, se queda corto frente a Holt.
""",
    ),
    (
        "Holt-Winters aditivo",
        """
Nivel + tendencia + temporada de **amplitud más o menos fija** (los picos suman la misma cantidad).

**Sirve cuando** diciembre o el verano siempre suman un monto parecido, aunque el negocio crezca poco.
""",
    ),
    (
        "Holt-Winters multiplicativo",
        """
La temporada **escala con el nivel**: si el negocio es más grande, el pico de diciembre también lo es.

**Sirve cuando** el alza de los meses altos crece con las ventas. Típico de retail y turismo.

**Requisito:** valores positivos.
""",
    ),
    (
        "ARIMA",
        """
Combina rezagos de la serie (AR), diferenciación (I) y rezagos del error (MA).
La app elige el orden con búsqueda automática, con parte estacional si hay historia suficiente.

**Sirve cuando** hay persistencia, necesidad de diferenciar o un patrón que el suavizado no captura bien.

**Lectura:** un ARIMA ganador no “explica” el negocio; gana si reduce error en la muestra de test.
""",
    ),
    (
        "Prophet",
        """
Descompone la serie en tendencia flexible (con posibles quiebres) y estacionalidades.
Es robusto a huecos y a cambios de nivel.

**Sirve cuando** hay temporada y la tendencia no es una recta. No sustituye a un modelo causal.

**Nota:** no reporta AIC comparable al de Holt o ARIMA.
""",
    ),
    (
        "SVR univariado",
        """
Máquina de vectores de soporte sobre **rezagos** de la misma serie. Busca una función no lineal
que explique el siguiente valor a partir de los anteriores.

**Sirve cuando** hay regularidades locales que un suavizado lineal no ve.

**Nota:** no tiene AIC; se juzga por el error en la muestra de entrenamiento y en la de test.
""",
    ),
    (
        "Bosque aleatorio (RF) univariado",
        """
Promedia muchos árboles entrenados sobre rezagos. Captura interacciones y umbrales.

**Sirve cuando** la relación con el pasado no es suave. Puede aplanarse fuera del rango visto en la muestra de entrenamiento.
""",
    ),
    (
        "XGBoost univariado",
        """
Árboles en secuencia que corrigen el error del anterior, también sobre rezagos.

**Sirve** en el mismo terreno que RF, a menudo con menos sesgo. Sigue siendo univariado:
no entra ni inflación ni pauta, solo la historia de la variable elegida.
""",
    ),
]

for titulo, cuerpo in bloques:
    with st.expander(titulo, expanded=False):
        st.markdown(cuerpo)

st.markdown("### Cómo se decide en esta mesa")
st.markdown(
    r"""
La serie se parte en **muestra de entrenamiento** (con ella se estima) y **muestra de test** (un tramo final que el modelo no ve).

| Métrica | Qué mira | Uso en la mesa |
|---------|----------|----------------|
| **RMSE** | Error cuadrático; castiga desvíos grandes | Criterio principal, en la muestra de test |
| **MAE** | Error absoluto medio | Más interpretable en la unidad de la serie |
| **MAPE** | Error porcentual | Comparar series de distinto nivel; se cae si hay ceros |
| **MASE** | Error frente a un ingenuo de un paso | Menor que 1: mejora al “último valor” |
| **AIC** | Ajuste en la muestra de entrenamiento, penalizado por parámetros | Complemento de SES/Holt/HW/ARIMA; no aplica a Prophet ni a ML |

Para **pronosticar**, gana quien falla menos en la muestra de test. El AIC (muestra de entrenamiento) no veta a un modelo que gana en test.
"""
)
