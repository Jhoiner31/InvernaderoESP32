import time
import config
import actuadores

modo = "auto"

suelo_min = config.SUELO_MIN
temp_max = config.TEMP_MAX
luz_min = config.LUZ_MIN

_ultimo_riego = None
_riego_activo = False

def actualizar(temp, hum_suelo, luz):
    global _ultimo_riego, _riego_activo

    if modo != "auto":
        return

    ahora = time.ticks_ms()

    # Riego por tiempo fijo
    if _riego_activo:
        if time.ticks_diff(ahora, _ultimo_riego) >= config.TIEMPO_RIEGO * 1000:
            actuadores.bomba(False)
            _riego_activo = False
    else:
        espera_cumplida = (_ultimo_riego is None or
                           time.ticks_diff(ahora, _ultimo_riego) >= config.TIEMPO_ESPERA * 1000)
        if hum_suelo < suelo_min and espera_cumplida:
            actuadores.bomba(True)
            _riego_activo = True
            _ultimo_riego = ahora

    # Ventilador por temperatura
    if temp is not None:
        actuadores.ventilador(temp > temp_max)

    # Luz de crecimiento por luz ambiente
    actuadores.luz(luz < luz_min)

def cambiar_modo(nuevo_modo):
    global modo, _riego_activo

    if nuevo_modo not in ("auto", "manual"):
        return False

    modo = nuevo_modo
    if modo == "manual":
        actuadores.bomba(False)
        _riego_activo = False
    return True

def comando_actuador(nombre, encendido):
    if modo != "manual":
        return False

    if nombre == "bomba":
        actuadores.bomba(encendido)
    elif nombre == "ventilador":
        actuadores.ventilador(encendido)
    elif nombre == "luz":
        actuadores.luz(encendido)
    else:
        return False
    return True

def cambiar_umbrales(nuevo_suelo, nueva_temp, nueva_luz):
    global suelo_min, temp_max, luz_min

    suelo_min = nuevo_suelo
    temp_max = nueva_temp
    luz_min = nueva_luz

def revisar_alertas(temp, hum_suelo):
    alertas = []

    if hum_suelo < config.SUELO_CRITICO:
        alertas.append({"tipo": "suelo_seco", "valor": hum_suelo})

    if temp is not None and temp > config.TEMP_CRITICA:
        alertas.append({"tipo": "temp_alta", "valor": temp})

    return alertas

_alertas_activas = []

def alertas_nuevas(alertas):
    global _alertas_activas

    nuevas = []
    tipos_ahora = []
    for alerta in alertas:
        tipos_ahora.append(alerta["tipo"])
        if alerta["tipo"] not in _alertas_activas:
            nuevas.append(alerta)

    _alertas_activas = tipos_ahora
    return nuevas