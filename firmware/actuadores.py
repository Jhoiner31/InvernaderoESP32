from machine import Pin, PWM
import config
import time

_bomba = Pin(config.PIN_BOMBA, Pin.OUT)
_ventilador = Pin(config.PIN_VENTILADOR, Pin.OUT)
_luz = Pin(config.PIN_LUZ_CRECIMIENTO, Pin.OUT)
_buzzer = PWM(Pin(config.PIN_BUZZER))

_bomba.value(0)
_ventilador.value(0)
_luz.value(0)
_buzzer.duty(0)

def bomba(encendida):
    _bomba.value(1 if encendida else 0)


def ventilador(encendido):
    _ventilador.value(1 if encendido else 0)


def luz(encendida):
    _luz.value(1 if encendida else 0)


def estado():
    return {
        "bomba": _bomba.value(),
        "ventilador": _ventilador.value(),
        "luz": _luz.value(),
    }

def pitido(duracion=0.3, frecuencia=1000):
    _buzzer.freq(frecuencia)
    _buzzer.duty(512)
    time.sleep(duracion)
    _buzzer.duty(0)