import control
import network
import time
import json
import secrets
import config
from umqtt.simple import MQTTClient

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        intentos = 0
        while not wlan.isconnected() and intentos < 20:
            time.sleep(0.5)
            intentos += 1

    return wlan.isconnected()

_cliente = None


def conectar_broker():
    global _cliente
    _cliente = MQTTClient(config.MQTT_CLIENT_ID, config.MQTT_BROKER,
                          port=config.MQTT_PUERTO)
    _cliente.set_last_will(config.TOPIC_CONEXION, b"offline", retain=True)
    try:
        _cliente.connect()
        _cliente.publish(config.TOPIC_CONEXION, b"online", retain=True)
        return True
    except OSError:
        _cliente = None
        return False


def publicar_sensores(temp, hum_aire, hum_suelo, luz):
    if _cliente is None:
        return False
    datos = {"temp": temp, "hum_aire": hum_aire,
             "hum_suelo": hum_suelo, "luz": luz}
    try:
        _cliente.publish(config.TOPIC_SENSORES, json.dumps(datos))
        return True
    except OSError:
        return False

def _al_recibir(topico, mensaje):
    topico = topico.decode()
    texto = mensaje.decode()
    print("Recibido:", topico, texto)

    if topico == config.TOPIC_CMD_MODO:
        control.cambiar_modo(texto)
    elif topico == config.TOPIC_CMD_BOMBA:
        control.comando_actuador("bomba", texto == "1")
    elif topico == config.TOPIC_CMD_VENTILADOR:
        control.comando_actuador("ventilador", texto == "1")
    elif topico == config.TOPIC_CMD_LUZ:
        control.comando_actuador("luz", texto == "1")
    elif topico == config.TOPIC_CMD_UMBRALES:
        try:
            u = json.loads(texto)
            control.cambiar_umbrales(u["suelo_min"], u["temp_max"], u["luz_min"])
        except (ValueError, KeyError):
            print("Umbrales invalidos")


def suscribirse():
    if _cliente is None:
        return False
    _cliente.set_callback(_al_recibir)
    for t in (config.TOPIC_CMD_MODO, config.TOPIC_CMD_BOMBA,
              config.TOPIC_CMD_VENTILADOR, config.TOPIC_CMD_LUZ,
              config.TOPIC_CMD_UMBRALES):
        _cliente.subscribe(t)
    return True


def revisar_mensajes():
    if _cliente is None:
        return
    try:
        _cliente.check_msg()
    except OSError:
        pass

def publicar_actuadores(estado, modo):
    if _cliente is None:
        return False
    datos = {"bomba": estado["bomba"], "ventilador": estado["ventilador"],
             "luz": estado["luz"], "modo": modo}
    try:
        _cliente.publish(config.TOPIC_ACTUADORES, json.dumps(datos))
        return True
    except OSError:
        return False


def publicar_alerta(alerta):
    if _cliente is None:
        return False
    try:
        _cliente.publish(config.TOPIC_ALERTAS, json.dumps(alerta))
        return True
    except OSError:
        return False