from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

OCULTAR = {"Series_ID", "Champion", "Country"}

CATALOGO = {
    "us_change": {
        "titulo": "Macro — ciclo, demanda y caja de los hogares",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "contexto": (
            "Tablero trimestral de la economía: cómo se mueve el gasto, el ingreso, la "
            "producción, el ahorro y el desempleo. Sirve para leer el ciclo antes de "
            "fijar metas de venta, cupos de crédito o una política de caja."
        ),
        "nombres": {
            "Consumption": "Consumo",
            "Income": "Ingreso disponible",
            "Production": "Producción",
            "Savings": "Ahorro",
            "Unemployment": "Desempleo",
        },
        "variables": {
            "Consumption": "Variación del consumo de los hogares. Proxy de demanda interna y de recaudo comercial.",
            "Income": "Variación del ingreso disponible. Capacidad de pago y de gasto de las familias.",
            "Production": "Variación de la producción. Pulso de la actividad real y de la utilización de capacidad.",
            "Savings": "Variación del ahorro. Si sube el ahorro, el consumo (y la caja del mostrador) suele aflojarse.",
            "Unemployment": "Variación del desempleo. Señal de ciclo laboral, mora y demanda de bienes durables.",
        },
        "sugerida": "Consumption",
    },
    "insurance": {
        "titulo": "Seguros — cotizaciones y pauta",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 8,
        "contexto": (
            "Una aseguradora mira dos palancas del mismo presupuesto: las cotizaciones que "
            "entran (embudo comercial) y lo que se gasta en pauta. El error de pronóstico "
            "aquí es cupo de marketing mal puesto o una meta de primas inflada."
        ),
        "nombres": {
            "Quotes": "Cotizaciones",
            "TVadverts": "Gasto en pauta",
        },
        "variables": {
            "Quotes": "Cotizaciones emitidas en el mes. Volumen de entrada del canal comercial.",
            "TVadverts": "Gasto mensual en publicidad. Desembolso discrecional del presupuesto de marketing.",
        },
        "sugerida": "Quotes",
    },
    "souvenirs": {
        "titulo": "Retail — ventas de mostrador",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 12,
        "contexto": (
            "Ventas de un almacén de souvenirs en un destino de playa. Caso típico de "
            "mostrador con temporada: el mes pico define inventario, caja y personal."
        ),
        "nombres": {"Sales": "Ventas"},
        "variables": {
            "Sales": "Ventas del mes. Ingreso del canal comercial; base para metas e inventario.",
        },
        "sugerida": "Sales",
    },
    "canadian_gas": {
        "titulo": "Energía — producción de gas",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Producción mensual de gas. Interesa a planeación de oferta, contratos de "
            "suministro y la caja de un productor de commodities."
        ),
        "nombres": {"Volume": "Producción"},
        "variables": {
            "Volume": "Volumen producido en el mes. Oferta física que se traduce en ingreso si hay precio.",
        },
        "sugerida": "Volume",
    },
    "us_gasoline": {
        "titulo": "Energía — demanda de gasolina",
        "frecuencia": "semanal",
        "periodo": 52,
        "h": 16,
        "contexto": (
            "Suministro semanal de gasolina. Señal de demanda energética y de actividad "
            "de transporte: útil para inventario, cobertura y precio de un combustible."
        ),
        "nombres": {"Barrels": "Barriles"},
        "variables": {
            "Barrels": "Millones de barriles diarios. Volumen de demanda del combustible.",
        },
        "sugerida": "Barrels",
    },
    "us_employment": {
        "titulo": "Laboral — empleo por sector",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Nómina mensual por rama de la economía. El empleo del sector mueve masa salarial, "
            "demanda de crédito y primas de seguros; no es lo mismo manufactura que finanzas."
        ),
        "nombres": {"Employed": "Empleo"},
        "variables": {
            "Employed": "Personas ocupadas (miles). Nivel de actividad laboral y de masa salarial del sector.",
        },
        "entidades": ["Title"],
        "sugerida": "Employed",
        "entidad_sugerida": {"Title": "Total Private"},
    },
    "aus_airpassengers": {
        "titulo": "Transporte — pasajeros aéreos",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 5,
        "contexto": (
            "Pasajeros aéreos por año. Demanda de largo plazo para flota, slots y "
            "capex: un error aquí se paga en aviones de más o en capacidad corta."
        ),
        "nombres": {"Passengers": "Pasajeros"},
        "variables": {
            "Passengers": "Millones de pasajeros en el año. Demanda que sostiene tarifas, ocupación y capex.",
        },
        "sugerida": "Passengers",
    },
    "aus_arrivals": {
        "titulo": "Turismo — llegadas por mercado emisor",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "contexto": (
            "Llegadas internacionales por país de origen. Cada origen es un mercado: "
            "ocupación hotelera, tipo de cambio y el ingreso de divisas no se mueven igual."
        ),
        "nombres": {"Arrivals": "Llegadas"},
        "variables": {
            "Arrivals": "Viajeros que llegan en el trimestre. Demanda turística que alimenta hoteles, retail y caja en divisas.",
        },
        "entidades": ["Origin"],
        "sugerida": "Arrivals",
    },
    "aus_accommodation": {
        "titulo": "Hotelería — ingresos, ocupación e inflación",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "contexto": (
            "Alojamiento turístico por estado: lo que entra a caja, cuántas habitaciones "
            "se ocupan y el IPC de fondo. Tres lecturas para tarifa, occupancy y margen."
        ),
        "nombres": {
            "Takings": "Ingresos hoteleros",
            "Occupancy": "Ocupación",
            "CPI": "IPC",
        },
        "variables": {
            "Takings": "Ingresos del alojamiento. Caja del sector hotelero.",
            "Occupancy": "Habitaciones ocupadas (%). Uso de la capacidad instalada y palanca de tarifa.",
            "CPI": "Índice de precios. Contexto inflacionario para costos y reajuste de tarifas.",
        },
        "entidades": ["State"],
        "sugerida": "Takings",
    },
    "aus_vehicle_sales": {
        "titulo": "Bienes durables — ventas de vehículos",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Vehículos nuevos por tipo (pasajeros, SUV u otros). Bien durable sensible a "
            "crédito, tasas y confianza: mueve inventario de concesionarios y la cartera de la banca."
        ),
        "nombres": {"Count": "Unidades vendidas"},
        "variables": {
            "Count": "Vehículos vendidos en el mes. Volumen del mercado automotor y de la colocación de crédito de consumo.",
        },
        "entidades": ["Type"],
        "sugerida": "Count",
    },
    "aus_tobacco": {
        "titulo": "Consumo gravado — gasto en tabaco",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "contexto": (
            "Gasto real de los hogares en tabaco, por estado. Bien regulado y gravado: "
            "sirve para recaudo, inventario de un canal cautivo y la lectura de un consumo que no sigue al retail general."
        ),
        "nombres": {"Expenditure": "Gasto"},
        "variables": {
            "Expenditure": "Gasto real en tabaco. Demanda de un consumo gravado; base de recaudo e inventario.",
        },
        "entidades": ["State"],
        "sugerida": "Expenditure",
    },
    "aus_births": {
        "titulo": "Demografía — nacimientos y demanda futura",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Nacimientos por estado. No es una venta, pero fija la demanda de largo plazo "
            "de vivienda, colegios, salud y seguros de vida. Un presupuesto público o un "
            "asegurador lo lee como flujo de nuevos afiliados."
        ),
        "nombres": {"Births": "Nacimientos"},
        "variables": {
            "Births": "Nacimientos del mes. Flujo demográfico que anticipa demanda de servicios y de seguros.",
        },
        "entidades": ["State"],
        "sugerida": "Births",
    },
    "aus_migration": {
        "titulo": "Demografía — saldo migratorio",
        "frecuencia": "trimestral",
        "periodo": 4,
        "h": 8,
        "contexto": (
            "Migración neta por estado. Impulso (o fuga) de población en edad de trabajar: "
            "mueve vivienda, consumo, masa salarial y la base de cotizantes."
        ),
        "nombres": {"NOM": "Saldo migratorio"},
        "variables": {
            "NOM": "Ganancia o pérdida neta de población. Impulso de demanda local y de la fuerza laboral.",
        },
        "entidades": ["State"],
        "sugerida": "NOM",
    },
    "aus_inbound": {
        "titulo": "Turismo — visitantes y gasto en destino",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Visitantes de corto plazo por país y motivo del viaje. Cada segmento es un "
            "flujo de divisas distinto: ocio no gasta igual que negocios. Sirve para hoteles, "
            "retail y la caja del destino."
        ),
        "nombres": {"Count": "Visitantes"},
        "variables": {
            "Count": "Personas que llegan en el mes. Demanda turística del segmento y proxy del gasto en destino.",
        },
        "entidades": ["Country", "Purpose"],
        "sugerida": "Count",
    },
    "aus_outbound": {
        "titulo": "Turismo — gasto de residentes en el exterior",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Residentes que salen, por destino y motivo. Es fuga de gasto: lo que no se "
            "consume en el país. Interesa a aerolíneas, tipo de cambio y al retail local que pierde esa demanda."
        ),
        "nombres": {"Count": "Salidas"},
        "variables": {
            "Count": "Residentes que salen en el mes. Demanda de viaje al exterior y fuga de consumo doméstico.",
        },
        "entidades": ["Country", "Purpose"],
        "sugerida": "Count",
    },
    "aus_fertility": {
        "titulo": "Demografía — fecundidad y largo plazo",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 5,
        "contexto": (
            "Tasa de fecundidad por región y edad. Serie estructural: pensiones, mercado "
            "laboral y la demanda de vivienda de aquí a dos décadas se leen con esto, no con un mes de ventas."
        ),
        "nombres": {"Rate": "Fecundidad"},
        "variables": {
            "Rate": "Nacimientos por mil mujeres. Indicador de la base futura de cotizantes y de demanda de largo plazo.",
        },
        "entidades": ["Region", "Age"],
        "sugerida": "Rate",
    },
    "aus_mortality": {
        "titulo": "Riesgo — mortalidad y seguros de vida",
        "frecuencia": "semanal",
        "periodo": 52,
        "h": 16,
        "contexto": (
            "Muertes y tasa de mortalidad por sexo y edad. Tablero de un asegurador o de "
            "un fondo: siniestralidad, reservas y el costo de las coberturas de vida."
        ),
        "nombres": {
            "Deaths": "Siniestros (muertes)",
            "Mortality": "Tasa de mortalidad",
        },
        "variables": {
            "Deaths": "Muertes en la semana. Volumen de siniestros para un portafolio de vida.",
            "Mortality": "Muertes por mil. Tasa de riesgo: base para prima y reserva.",
        },
        "entidades": ["Sex", "Age"],
        "sugerida": "Mortality",
    },
    "ny_childcare": {
        "titulo": "Servicios — empleo en cuidado infantil",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Nómina del cuidado infantil en una ciudad grande. Sector de servicios locales: "
            "masa salarial, costo de un insumo de las familias y señal de la actividad urbana."
        ),
        "nombres": {"Count": "Empleo"},
        "variables": {
            "Count": "Empleados (miles). Nómina del sector: costo laboral y pulso de un servicio esencial.",
        },
        "sugerida": "Count",
    },
    "nsw_offences": {
        "titulo": "Riesgo operativo — incidentes reportados",
        "frecuencia": "mensual",
        "periodo": 12,
        "h": 18,
        "contexto": (
            "Incidentes por tipo. Para un asegurador, un municipio o un retailer es costo "
            "de seguridad, prima de riesgo y asignación de recursos. Cada tipo es una exposición distinta."
        ),
        "nombres": {"Count": "Incidentes"},
        "variables": {
            "Count": "Casos reportados en el mes. Volumen de exposición: mueve costo de seguridad y prima de riesgo.",
        },
        "entidades": ["Type"],
        "sugerida": "Count",
    },
    "prices": {
        "titulo": "Commodities — precios reales",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 8,
        "contexto": (
            "Precios anuales ajustados por inflación (alimentos, metales, energía, trigo). "
            "Sirven para cobertura, inventario y la lectura de un insumo en el costo de un negocio."
        ),
        "nombres": {
            "eggs": "Huevos",
            "chicken": "Pollo",
            "copper": "Cobre",
            "nails": "Clavos",
            "oil": "Petróleo",
            "wheat": "Trigo",
        },
        "variables": {
            "eggs": "Precio real de los huevos. Insumo alimentario; costo de un canal de alimentos.",
            "chicken": "Precio real del pollo. Proteína: costo de inventario y de menú.",
            "copper": "Precio real del cobre. Metal industrial; capex y construcción.",
            "nails": "Precio real de los clavos. Insumo de construcción y ferretería.",
            "oil": "Precio real del petróleo. Energía y flete: mueve margen de casi cualquier cadena.",
            "wheat": "Precio real del trigo. Grano: costo de alimentos y de cobertura agrícola.",
        },
        "sugerida": "oil",
    },
    "guinea_rice": {
        "titulo": "Commodities — producción de arroz",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 5,
        "contexto": (
            "Producción anual de arroz. Oferta de un alimento básico: precio interno, "
            "importaciones y la caja de un comercializador agrícola."
        ),
        "nombres": {"Production": "Producción"},
        "variables": {
            "Production": "Millones de toneladas en el año. Oferta del grano; base de precio y de abastecimiento.",
        },
        "sugerida": "Production",
    },
    "boston_marathon": {
        "titulo": "Patrocinio — desempeño de un evento",
        "frecuencia": "anual",
        "periodo": 1,
        "h": 8,
        "contexto": (
            "Tiempo ganador de un evento anual masivo, por categoría. Para un patrocinador "
            "o un organizador es la serie de desempeño que sostiene derechos, audiencia y renovación de contratos."
        ),
        "nombres": {"Time": "Tiempo (segundos)"},
        "variables": {
            "Time": "Tiempo ganador en segundos. Indicador de desempeño del evento; se pronostica el nivel, no un flujo de caja.",
        },
        "entidades": ["Event"],
        "sugerida": "Time",
    },
    "melb_walkers": {
        "titulo": "Retail urbano — afluencia peatonal",
        "frecuencia": "diaria",
        "periodo": 7,
        "h": 21,
        "contexto": (
            "Peatones diarios en el centro. Proxy de afluencia: ventas de calle, arriendos "
            "comerciales y la caja de un local que vive del tráfico. Tiene patrón de semana y quiebres de ciudad."
        ),
        "nombres": {"Count": "Afluencia"},
        "variables": {
            "Count": "Peatones promedio del día. Tráfico del punto: anticipa venta de mostrador y ocupación comercial.",
        },
        "sugerida": "Count",
    },
    "otexts_views": {
        "titulo": "Digital — visitas y demanda de contenido",
        "frecuencia": "diaria",
        "periodo": 7,
        "h": 21,
        "contexto": (
            "Visitas diarias a un sitio. Demanda digital: pauta, conversión y la caja de "
            "un canal que se monetiza por tráfico. Hay temporada de semana y picos de campaña."
        ),
        "nombres": {"Pageviews": "Visitas"},
        "variables": {
            "Pageviews": "Páginas vistas en el día. Demanda de contenido; base de pauta y de conversión.",
        },
        "sugerida": "Pageviews",
    },
}


def ids_ordenados():
    return list(CATALOGO.keys())


def etiqueta(dataset_id: str) -> str:
    meta = CATALOGO[dataset_id]
    return f"{meta['titulo']}  ·  {meta['frecuencia']}"


ETIQUETAS_ENTIDAD = {
    "Title": "Sector",
    "Origin": "Mercado emisor",
    "State": "Estado / región",
    "Type": "Tipo",
    "Country": "País",
    "Purpose": "Motivo del viaje",
    "Region": "Región",
    "Age": "Edad",
    "Sex": "Sexo",
    "Event": "Categoría",
}


def nombre_variable(dataset_id: str, col: str) -> str:
    return CATALOGO.get(dataset_id, {}).get("nombres", {}).get(col, col)


def etiqueta_entidad(col: str) -> str:
    return ETIQUETAS_ENTIDAD.get(col, col)
