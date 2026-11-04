from machine import Pin, ADC
import dht
import config

#Crea el objeto sensor
_dht = dht.DHT22(Pin(config.PIN_DHT))

#Configura esos pines como analogicos
_luz = ADC(Pin(config.PIN_LUZ))
_suelo = ADC(Pin(config.PIN_SUELO))

#Configura la ESP32 para que entienda los voltajes de los sensores
_suelo.atten(ADC.ATTN_11DB)
_luz.atten(ADC.ATTN_11DB)

#Funcion que define el porcentaje de luz y humedad
def _a_porcentaje(valor, minimo, maximo):
    porcentaje = ((valor - minimo)/(maximo - minimo))*100

    if porcentaje < 0:
        porcentaje = 0

    elif porcentaje > 100:
        porcentaje = 100

    return round(porcentaje)

#Funcion que activa el sensor de temperatura y humedad en el aire
def leer_dht():
    try:
        _dht.measure()
        return _dht.temperature(), _dht.humidity()
    except OSError:
        return None, None

#Funcion que mide porcentaje de humeda en el suelo
def leer_suelo():
    crudo = _suelo.read()
    return _a_porcentaje(crudo, config.SUELO_SECO, config.SUELO_MOJADO)

#Funcion que mide porcentaje de luz
def leer_luz():
    crudo = _luz.read()
    return _a_porcentaje(crudo, config.LUZ_OSCURO, config.LUZ_BRILLANTE)