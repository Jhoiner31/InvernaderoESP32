"""Ajustes generales de la interfaz.

Aqui van los valores que se repiten en varios archivos (colores, umbrales,
nombres de variables...). Asi, si hay que cambiar algo, se cambia en un solo lugar.
Los valores de umbrales y tiempos son los mismos del firmware (firmware/config.py).
"""

# ---------- Apariencia ----------
FUENTE = "Segoe UI"
COLORES = {
    "fondo": "#0d1117",
    "panel": "#161b22",
    "borde": "#30363d",
    "texto": "#e6edf3",
    "tenue": "#8b949e",
    "acento": "#388bfd",
    "ok": "#3fb950",         # verde    -> normal
    "aviso": "#d29922",      # amarillo -> precaución
    "crit": "#f85149",       # rojo     -> crítico
    "fila_alerta": "#3d1418",
}
TEXTO_ESTADO = {"ok": "Normal", "aviso": "Precaución", "crit": "Crítico"}

# ---------- Valores del firmware ----------
UMBRALES_INICIALES = {"suelo_min": 35, "temp_max": 30, "luz_min": 40}
TIEMPO_RIEGO = 5      # s que dura el riego
TIEMPO_ESPERA = 30    # s de espera antes de volver a regar
CRIT_SUELO = 20       # % por debajo -> alerta
CRIT_TEMP = 35        # °C por encima -> alerta

# ---------- Contenido de la pantalla ----------
# Tarjetas del monitor: (clave, titulo, unidad)
SENSORES = [
    ("temp", "Temperatura", "°C", 50, 1, "ok"),
    ("hum_aire", "Humedad del aire", "%", 100, 0, "ok"),
    ("hum_suelo", "Humedad del suelo", "%", 100, 0, "ok"),
    ("luz", "Luz ambiente", "%", 100, 0, "ok")
]

# Actuadores: (clave, etiqueta)
ACTUADORES = [
    ("bomba", "Bomba de riego"),
    ("ventilador", "Ventilador"),
    ("luz", "Luz de crecimiento"),
]

# Campos de umbrales: (clave, nombre, unidad, minimo, maximo)
UMBRALES_CAMPOS = [
    ("suelo_min", "Humedad mínima del suelo", "%", 0, 100),
    ("temp_max", "Temperatura máxima", "°C", 15, 50),
    ("luz_min", "Luz mínima", "%", 0, 100),
]

# Variables graficables: nombre -> (clave, unidad, (ymin, ymax), color)
VARIABLES = ["Temperatura (°C)", "Humedad del aire (%)",
             "Humedad del suelo (%)", "Luz (%)"]
RANGOS = ["1 min", "10 min", "1 h"]

NOMBRES_ALERTA = {"suelo_seco": "Suelo muy seco", "temp_alta": "Temperatura muy alta"}
TEXTO_ACTUADORES = {
    "bomba": ("Riego activado", "Riego detenido"),
    "ventilador": ("Ventilador encendido", "Ventilador apagado"),
    "luz": ("Luz de crecimiento encendida", "Luz de crecimiento apagada"),
}
MODOS = ["auto", "manual"]

# Historial
RANGOS_HISTORIAL = ["Última hora", "Últimas 24 h", "Últimos 7 días", "Todo"]
COLUMNAS_HISTORIAL = ["Fecha y hora", "Temperatura (°C)", "Humedad del aire (%)",
                      "Humedad del suelo (%)", "Luz (%)"]