# Pines de entrada
PIN_DHT = 4
PIN_SUELO = 34
PIN_LUZ = 35

# Calibracion del ADC (valores crudos de 0 a 4095)
SUELO_SECO = 4095
SUELO_MOJADO = 1500
LUZ_OSCURO = 0
LUZ_BRILLANTE = 4095

# Cada cuantos segundos se leen los sensores
INTERVALO_LECTURA = 2

# Pines de salida
PIN_BOMBA = 26
PIN_VENTILADOR = 27
PIN_LUZ_CRECIMIENTO = 25
PIN_BUZZER = 14

# Umbrales del modo automatico (valores iniciales)
SUELO_MIN = 35
TEMP_MAX = 30
LUZ_MIN = 40

# Tiempos del riego (en segundos)
TIEMPO_RIEGO = 5
TIEMPO_ESPERA = 30

# Umbrales criticos (para alertas)
SUELO_CRITICO = 20
TEMP_CRITICA = 35

# MQTT
MQTT_BROKER = "test.mosquitto.org"
MQTT_PUERTO = 1883
MQTT_CLIENT_ID = "invernadero_jhoiner_mateo"
TOPIC_SENSORES = "invernadero_utp_g105/sensores"

TOPIC_CMD_MODO = "invernadero_utp_g105/cmd/modo"
TOPIC_CMD_BOMBA = "invernadero_utp_g105/cmd/bomba"
TOPIC_CMD_VENTILADOR = "invernadero_utp_g105/cmd/ventilador"
TOPIC_CMD_LUZ = "invernadero_utp_g105/cmd/luz"
TOPIC_CMD_UMBRALES = "invernadero_utp_g105/cmd/umbrales"

TOPIC_ACTUADORES = "invernadero_utp_g105/actuadores/estado"
TOPIC_ALERTAS = "invernadero_utp_g105/alertas"
TOPIC_CONEXION = "invernadero_utp_g105/conexion"
