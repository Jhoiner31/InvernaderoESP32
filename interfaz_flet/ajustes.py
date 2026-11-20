"""Ajustes generales de la interfaz.

Aqui van los valores que se repiten en varios archivos (colores, umbrales,
nombres de variables...). Asi, si hay que cambiar algo, se cambia en un solo lugar.
Los valores de umbrales y tiempos son los mismos del firmware (firmware/config.py).
"""
import os

# ---------- Apariencia ----------
FUENTE = "Segoe UI"
PALETAS = {
    "oscuro": {
        "fondo": "#0f1a14",
        "panel": "#16241c",
        "borde": "#26382d",
        "texto": "#e4efe7",
        "tenue": "#8fa89a",
        "acento": "#5fae7e",
        "ok": "#4caf7a",
        "aviso": "#d9b44a",
        "crit": "#e0645c",
    },
    "claro": {
        "fondo": "#f1f6f2",
        "panel": "#ffffff",
        "borde": "#d5e2d8",
        "texto": "#1f2d25",
        "tenue": "#5f7568",
        "acento": "#3f8f62",
        "ok": "#2e8b57",
        "aviso": "#b98a14",
        "crit": "#c8453d",
    },
}
TEXTO_ESTADO = {"ok": "Normal", "aviso": "Precaución", "crit": "Crítico"}

# ---------- Valores del firmware ----------
UMBRALES_INICIALES = {"suelo_min": 35, "temp_max": 30, "luz_min": 40}
TIEMPO_RIEGO = 5      # s que dura el riego
TIEMPO_ESPERA = 30    # s de espera antes de volver a regar
CRIT_SUELO = 20       # % por debajo -> alerta
CRIT_TEMP = 35        # °C por encima -> alerta

# ---------- Comportamiento de la interfaz ----------
INTERVALO_MS = 1000       # cada cuanto llega un dato simulado
TIMEOUT_CONEXION = 10     # s sin datos -> "Sin conexión"

# Campos de umbrales: (clave, nombre, unidad, minimo, maximo)
UMBRALES_CAMPOS = [
    ("suelo_min", "Humedad mínima del suelo", "%", 0, 100),
    ("temp_max", "Temperatura máxima", "°C", 15, 50),
    ("luz_min", "Luz mínima", "%", 0, 100),
]

# Variables graficables: nombre -> (clave, unidad, (ymin, ymax), color)
VARIABLES = {
    "Temperatura (°C)": ("temp", "°C", (10, 50), "#f0883e"),
    "Humedad del aire (%)": ("hum_aire", "%", (0, 100), "#58a6ff"),
    "Humedad del suelo (%)": ("hum_suelo", "%", (0, 100), "#3fb950"),
    "Luz (%)": ("luz", "%", (0, 100), "#e3b341"),
}
RANGOS = {"1 min": 60, "10 min": 600, "1 h": 3600}

NOMBRES_ALERTA = {"suelo_seco": "Suelo muy seco", "temp_alta": "Temperatura muy alta"}
TEXTO_ACTUADORES = {
    "bomba": ("Riego activado", "Riego detenido"),
    "ventilador": ("Ventilador encendido", "Ventilador apagado"),
    "luz": ("Luz de crecimiento encendida", "Luz de crecimiento apagada"),
}

# ---------- Historial ----------
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(CARPETA, "datos", "historial.csv")
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
COLUMNAS_CSV = ["fecha", "temp", "hum_aire", "hum_suelo", "luz",
                "modo", "bomba", "ventilador", "luz_crecimiento"]
