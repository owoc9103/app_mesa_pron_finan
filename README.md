# Mesa de pronóstico

Aplicación Streamlit para comparar modelos de series de tiempo.

## Cómo correrla

```bash
pip install -r requirements.txt
streamlit run Inicio.py
```

## Páginas

1. **Inicio** — para qué es la mesa.
2. **Los modelos** — SES, Holt, Holt amortiguado, HW aditivo y multiplicativo, ARIMA, Prophet, SVR, RF y XGBoost.
3. **La serie** — elige una base, lee el contexto y grafica una variable.
4. **La decisión** — muestra de entrenamiento y muestra de test, los diez modelos, RMSE/MAE/MAPE/MASE en ambas, AIC cuando aplica, y un modelo de trabajo.
