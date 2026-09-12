from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

OCULTAR = {"Series_ID", "Champion", "Country"}

CATALOGO = {
    "us_change": {
        "titulo": "Estados Unidos — cambios macroeconómicos",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "fuente": "Federal Reserve Bank of St. Louis",
        "contexto": (
            "Cambios porcentuales trimestrales (1970–2016) de consumo, ingreso disponible, "
            "producción, ahorro y desempleo en Estados Unidos. Los valores originales estaban "
            "en dólares encadenados de 2012. Sirve para ver si una variable real se mueve "
            "con tendencia, si es ruidosa o si reacciona a ciclos."
        ),
        "variables": {
            "Consumption": "Variación porcentual del consumo personal. Proxy de demanda interna.",
            "Income": "Variación del ingreso personal disponible. Capacidad de gasto de los hogares.",
            "Production": "Variación de la producción. Pulso de la actividad real.",
            "Savings": "Variación del ahorro. A menudo más volátil que el consumo.",
            "Unemployment": "Variación de la tasa de desempleo (puntos). Señal de ciclo laboral.",
        },
        "sugerida": "Consumption",
    },
    "insurance": {
        "titulo": "Seguros — cotizaciones y pauta en televisión",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 8,
        "fuente": "Aseguradora de EE. UU. (Dave Reilly, Automatic Forecasting Systems)",
        "contexto": (
            "Cotizaciones mensuales y gasto en publicidad televisiva de una aseguradora "
            "estadounidense (ene 2002–abr 2005). La gerencia suele preguntarse si la pauta "
            "anticipa las cotizaciones o si estas tienen vida propia."
        ),
        "variables": {
            "Quotes": "Número de cotizaciones emitidas en el mes. Variable comercial de entrada.",
            "TVadverts": "Gasto mensual en publicidad televisiva. Palanca discrecional de marketing.",
        },
        "sugerida": "Quotes",
    },
    "souvenirs": {
        "titulo": "Retail — ventas de un almacén de souvenirs",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 12,
        "fuente": "Makridakis, Wheelwright y Hyndman (1998)",
        "contexto": (
            "Ventas mensuales de un almacén de souvenirs en el muelle de un pueblo costero "
            "de Queensland, Australia. Típico caso de mostrador con temporada alta y baja: "
            "útil para cupos de inventario y caja del mes pico."
        ),
        "variables": {
            "Sales": "Ventas mensuales del almacén. Serie de ingreso del canal comercial.",
        },
        "sugerida": "Sales",
    },
    "canadian_gas": {
        "titulo": "Canadá — producción de gas",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "Hyndman, Koehler, Ord y Snyder (2008)",
        "contexto": (
            "Producción mensual de gas canadiense, en miles de millones de metros cúbicos "
            "(ene 1960–feb 2005). Interesa a planeación de oferta energética: tendencia de "
            "largo plazo y estacionalidad de demanda."
        ),
        "variables": {
            "Volume": "Volumen producido en el mes. Oferta física del commodity.",
        },
        "sugerida": "Volume",
    },
    "us_gasoline": {
        "titulo": "Estados Unidos — gasolina terminada",
        "frecuencia": "semanal",
        "periodo": 52,
        "h": 26,
        "fuente": "U.S. Energy Information Administration",
        "contexto": (
            "Suministro semanal de gasolina terminada en EE. UU., en millones de barriles "
            "por día (1991–2017). Serie de alta frecuencia para un commodity de consumo masivo."
        ),
        "variables": {
            "Barrels": "Millones de barriles diarios equivalentes. Señal de demanda energética.",
        },
        "sugerida": "Barrels",
    },
    "us_employment": {
        "titulo": "Estados Unidos — empleo por sector",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "U.S. Bureau of Labor Statistics",
        "contexto": (
            "Empleo mensual por sector (1939–2019). Cada título es una rama de la economía. "
            "Elija un sector: nómina, reclutamiento y la lectura del ciclo no son iguales "
            "en manufactura que en servicios financieros."
        ),
        "variables": {
            "Employed": "Personas ocupadas en el sector (miles, según la serie). Nivel de actividad laboral.",
        },
        "entidades": ["Title"],
        "sugerida": "Employed",
        "entidad_sugerida": {"Title": "Total Private"},
    },
    "aus_airpassengers": {
        "titulo": "Australia — pasajeros aéreos",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 5,
        "fuente": "Banco Mundial",
        "contexto": (
            "Pasajeros aéreos anuales (millones), domésticos e internacionales, de aerolíneas "
            "registradas en Australia (1970–2016). Serie larga de tendencia: útil para "
            "capacidad, flota e inversión de largo plazo."
        ),
        "variables": {
            "Passengers": "Millones de pasajeros en el año. Demanda de transporte aéreo.",
        },
        "sugerida": "Passengers",
    },
    "aus_arrivals": {
        "titulo": "Australia — llegadas internacionales",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "fuente": "Tourism Research Australia",
        "contexto": (
            "Llegadas trimestrales a Australia desde Japón, Nueva Zelanda, Reino Unido y "
            "Estados Unidos (1981–2012). Cada origen es un mercado emisor distinto."
        ),
        "variables": {
            "Arrivals": "Número de llegadas en el trimestre. Demanda turística por origen.",
        },
        "entidades": ["Origin"],
        "sugerida": "Arrivals",
    },
    "aus_accommodation": {
        "titulo": "Australia — alojamiento turístico",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "fuente": "Australian Bureau of Statistics",
        "contexto": (
            "Alojamiento turístico de corto plazo (15 o más habitaciones), 1998–2016, por estado. "
            "Takings son ingresos en millones de dólares australianos; Occupancy es el "
            "porcentaje de habitaciones ocupadas; CPI es el índice de precios (100 = 2012 T1)."
        ),
        "variables": {
            "Takings": "Ingresos del alojamiento (millones de AUD). Caja del sector hotelero.",
            "Occupancy": "Ocupación de habitaciones (%). Uso de capacidad instalada.",
            "CPI": "Índice de precios al consumidor de Australia. Contexto inflacionario.",
        },
        "entidades": ["State"],
        "sugerida": "Takings",
    },
    "aus_vehicle_sales": {
        "titulo": "Australia — ventas de vehículos nuevos",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "Australian Bureau of Statistics",
        "contexto": (
            "Vehículos nuevos vendidos en Australia (1994–2017), por tipo: pasajeros, SUV u otros. "
            "Serie de bien duradero, sensible a crédito, confianza y temporada."
        ),
        "variables": {
            "Count": "Unidades vendidas en el mes. Volumen del mercado automotor.",
        },
        "entidades": ["Type"],
        "sugerida": "Count",
    },
    "aus_tobacco": {
        "titulo": "Australia — gasto en cigarrillos y tabaco",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "fuente": "Australian Bureau of Statistics",
        "contexto": (
            "Gasto de los hogares en cigarrillos y tabaco, en volumen encadenado (miles de "
            "millones), 1985–2023, por estado. Consumo de un bien regulado, con tendencia "
            "de largo plazo distinta a la de un retail convencional."
        ),
        "variables": {
            "Expenditure": "Gasto real en tabaco. Demanda de un consumo gravado y regulado.",
        },
        "entidades": ["State"],
        "sugerida": "Expenditure",
    },
    "aus_births": {
        "titulo": "Australia — nacimientos",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "Australian Bureau of Statistics",
        "contexto": (
            "Nacimientos mensuales por estado y territorio (1975–2021). Serie demográfica "
            "con estacionalidad; importa a salud, educación y proyección de demanda local."
        ),
        "variables": {
            "Births": "Número de nacimientos en el mes. Flujo demográfico.",
        },
        "entidades": ["State"],
        "sugerida": "Births",
    },
    "aus_migration": {
        "titulo": "Australia — migración neta",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "fuente": "Australian Bureau of Statistics",
        "contexto": (
            "Migración neta en el exterior (NOM) por estado, 1981–2023. Es la ganancia o "
            "pérdida de población por inmigración y emigración (estadía de 12 meses o más)."
        ),
        "variables": {
            "NOM": "Saldo migratorio del trimestre. Impulso (o fuga) de población.",
        },
        "entidades": ["State"],
        "sugerida": "NOM",
    },
    "aus_inbound": {
        "titulo": "Australia — visitantes de corto plazo",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "Tourism Research Australia",
        "contexto": (
            "Llegadas mensuales de visitantes de corto plazo (menos de un año), 2005–2020, "
            "por país de residencia y motivo del viaje. Cada cruce es un segmento de demanda."
        ),
        "variables": {
            "Count": "Personas que llegan en el mes. Demanda turística del segmento.",
        },
        "entidades": ["Country", "Purpose"],
        "sugerida": "Count",
    },
    "aus_outbound": {
        "titulo": "Australia — residentes que salen",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "Tourism Research Australia",
        "contexto": (
            "Salidas mensuales de residentes australianos de corto plazo (2005–2017), "
            "por destino y motivo. Complemento de las llegadas: fuga de gasto turístico."
        ),
        "variables": {
            "Count": "Residentes que salen en el mes. Demanda de viaje al exterior.",
        },
        "entidades": ["Country", "Purpose"],
        "sugerida": "Count",
    },
    "aus_fertility": {
        "titulo": "Australia — fecundidad",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 5,
        "fuente": "Australian Bureau of Statistics",
        "contexto": (
            "Tasa de fecundidad anual (por mil mujeres), 1975–2022, por región y edad. "
            "Serie estructural, de movimiento lento: no se pronostica como una venta mensual."
        ),
        "variables": {
            "Rate": "Nacimientos por mil mujeres en el grupo. Indicador demográfico.",
        },
        "entidades": ["Region", "Age"],
        "sugerida": "Rate",
    },
    "aus_mortality": {
        "titulo": "Australia — mortalidad semanal",
        "frecuencia": "semanal",
        "periodo": 52,
        "h": 26,
        "fuente": "Human Mortality Database (STMF)",
        "contexto": (
            "Muertes y tasa de mortalidad semanal (2015–2023) por sexo y grupo de edad. "
            "La tasa es muertes por mil personas en la semana. Útil para riesgo y seguros de vida."
        ),
        "variables": {
            "Deaths": "Conteo semanal de muertes.",
            "Mortality": "Tasa de mortalidad semanal (por mil).",
        },
        "entidades": ["Sex", "Age"],
        "sugerida": "Mortality",
    },
    "ny_childcare": {
        "titulo": "Nueva York — empleo en guarderías",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "BLS / FRED",
        "contexto": (
            "Empleados (miles) en servicios de cuidado infantil en Nueva York, ene 1990–abr 2024. "
            "Serie laboral de un servicio local, sensible a demografía y a la actividad de la ciudad."
        ),
        "variables": {
            "Count": "Empleados en miles. Nómina del sector de cuidado infantil.",
        },
        "sugerida": "Count",
    },
    "nsw_offences": {
        "titulo": "Nueva Gales del Sur — delitos reportados",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "fuente": "NSW Bureau of Crime Statistics and Research",
        "contexto": (
            "Delitos mensuales reportados en NSW (1995–2023), por tipo. Cada tipo es una "
            "serie operativa distinta para asignación de recursos."
        ),
        "variables": {
            "Count": "Número de delitos reportados en el mes.",
        },
        "entidades": ["Type"],
        "sugerida": "Count",
    },
    "prices": {
        "titulo": "Commodities — precios reales",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 8,
        "fuente": "Makridakis, Wheelwright y Hyndman (1998)",
        "contexto": (
            "Precios anuales ajustados por inflación: huevos, pollo, cobre, clavos, petróleo "
            "(USD) y trigo (libras esterlinas). Series largas de commodities para ver "
            "tendencias de décadas, no el ruido de un mes."
        ),
        "variables": {
            "eggs": "Precio real de los huevos (USD).",
            "chicken": "Precio real del pollo (USD).",
            "copper": "Precio real del cobre (USD).",
            "nails": "Precio real de los clavos (USD).",
            "oil": "Precio real del petróleo (USD).",
            "wheat": "Precio real del trigo (libras esterlinas).",
        },
        "sugerida": "oil",
    },
    "guinea_rice": {
        "titulo": "Guinea — producción de arroz",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 5,
        "fuente": "Banco Mundial",
        "contexto": (
            "Producción anual de arroz en Guinea, millones de toneladas métricas (1970–2011). "
            "Serie de commodity agrícola de baja frecuencia."
        ),
        "variables": {
            "Production": "Millones de toneladas en el año. Oferta agrícola.",
        },
        "sugerida": "Production",
    },
    "boston_marathon": {
        "titulo": "Boston — tiempo del maratón",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 8,
        "fuente": "Boston Athletic Association",
        "contexto": (
            "Tiempo ganador del maratón de Boston (1897–2019), en segundos, por tipo de prueba. "
            "Serie larga de desempeño; el campeón cambia cada año, la prueba es la serie."
        ),
        "variables": {
            "Time": "Tiempo ganador en segundos. Menor es mejor en el deporte; aquí se pronostica el nivel.",
        },
        "entidades": ["Event"],
        "sugerida": "Time",
    },
    "melb_walkers": {
        "titulo": "Melbourne — peatones",
        "frecuencia": "diaria",
        "periodo": 7,
        "h": 28,
        "fuente": "Melbourne Open Data Portal",
        "contexto": (
            "Promedio diario de peatones en sensores de Melbourne (2019–2024). Serie de "
            "actividad urbana, con patrón semanal y quiebres (por ejemplo, 2020)."
        ),
        "variables": {
            "Count": "Peatones promedio del día. Flujo de la ciudad.",
        },
        "sugerida": "Count",
    },
    "otexts_views": {
        "titulo": "Sitio web — visitas diarias",
        "frecuencia": "diaria",
        "periodo": 7,
        "h": 28,
        "fuente": "Google Analytics / OTexts",
        "contexto": (
            "Visitas diarias a un sitio web. Serie digital con estacionalidad semanal "
            "y picos de tráfico."
        ),
        "variables": {
            "Pageviews": "Páginas vistas en el día. Demanda de contenido.",
        },
        "sugerida": "Pageviews",
    },
}


def ids_ordenados():
    return list(CATALOGO.keys())


def etiqueta(dataset_id: str) -> str:
    meta = CATALOGO[dataset_id]
    return f"{meta['titulo']}  ·  {meta['frecuencia']}"
