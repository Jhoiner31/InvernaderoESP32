"""Simulador del invernadero: hace de ESP32 mientras no hay conexión real.

Cada vez que se llama a paso() avanza un instante: mueve los sensores,
aplica la lógica automática y devuelve lo que "publicaría" la ESP32.
"""
import math
import random
import time

import ajustes as aj

def limitar(valor, minimo, maximo):
    """Obliga a que 'valor' quede entre 'minimo' y 'maximo'."""
    return max(minimo, min(maximo, valor))


class Simulador:
    def __init__(self):
        # Valores actuales de los sensores (cambian en cada paso)
        self.temp = 24.0
        self.hum_aire = 62.0
        self.hum_suelo = 55.0
        self.luz = 60.0

        # Estado del controlador
        self.modo = "auto"                              # "auto" o "manual"
        self.umbrales = dict(aj.UMBRALES_INICIALES)     # límites del modo automático
        self.actuadores = {"bomba": 0, "ventilador": 0, "luz": 0}   # 1 = encendido
        self.publicando = True      # False = se simula que se cortó la comunicación

        # Datos internos (el guion bajo indica "solo para uso de esta clase")
        self._inicio = time.time()          # para calcular cuánto tiempo lleva corriendo
        self._luz_natural = 50.0            # luz del "sol", sin contar la lámpara
        self._fin_riego = 0.0               # instante en que debe terminar el riego
        self._fin_espera = 0.0              # instante a partir del cual puede volver a regar
        self._calor_hasta = 0.0             # instante hasta el que dura el calor forzado
        self._alertas_activas = set()       # alertas que ya se avisaron y siguen activas

    # ------------------------------------------------------------------
    # Comandos (lo que la interfaz le "envía" a la ESP32)
    # ------------------------------------------------------------------
    def cambiar_modo(self, modo):
        self.modo = modo

    def comando(self, actuador, valor):
        """Enciende o apaga un actuador a mano. Solo funciona en modo manual."""
        if self.modo == "manual":
            self.actuadores[actuador] = int(valor)

    def aplicar_umbrales(self, umbrales):
        self.umbrales.update(umbrales)

    # Botones de demostración
    def forzar_suelo_seco(self):
        self.hum_suelo = 15.0

    def forzar_calor(self):
        self._calor_hasta = time.time() + 30    # 30 segundos de calor extra

    # ------------------------------------------------------------------
    # Un instante de la simulación
    # ------------------------------------------------------------------
    def paso(self):
        """Avanza un instante y devuelve el paquete de datos (o None si no hay comunicación)."""
        ahora = time.time()
        antes = dict(self.actuadores)       # copia, para detectar qué actuadores cambian

        self._mover_sensores(ahora)
        if self.modo == "auto":
            self._logica_automatica(ahora)

        eventos = self._eventos_actuadores(antes) + self._revisar_alertas()

        if not self.publicando:
            return None
        return {
            "sensores": {
                "temp": round(self.temp, 1),
                "hum_aire": round(self.hum_aire),
                "hum_suelo": round(self.hum_suelo),
                "luz": round(self.luz),
            },
            "actuadores": dict(self.actuadores),
            "modo": self.modo,
            "eventos": eventos,
        }

    # ------------------------------------------------------------------
    # Funciones internas
    # ------------------------------------------------------------------
    def _mover_sensores(self, ahora):
        """Cambia un poco cada sensor, teniendo en cuenta los actuadores."""
        t = ahora - self._inicio            # segundos desde que arrancó
        a = self.actuadores

        # Luz del sol: sube y baja suavemente (como el día). Va de 5 a 95.
        self._luz_natural = 50 + 45 * math.sin(t / 90)

        # Temperatura: tiende hacia la del ambiente; el ventilador la baja.
        ambiente = 28 + 3 * math.sin(t / 60)
        if ahora < self._calor_hasta:
            ambiente += 18
        self.temp += (ambiente - self.temp) * 0.08
        if a["ventilador"]:
            self.temp -= 0.6
        self.temp += random.uniform(-0.15, 0.15)            # pequeño ruido
        self.temp = limitar(self.temp, 5, 60)

        # Humedad del aire: oscila sola; el riego la sube y el ventilador la baja.
        objetivo = 60 + 10 * math.sin(t / 70 + 1)
        if a["bomba"]:
            objetivo += 5
        if a["ventilador"]:
            objetivo -= 8
        self.hum_aire += (objetivo - self.hum_aire) * 0.1 + random.uniform(-0.4, 0.4)
        self.hum_aire = limitar(self.hum_aire, 0, 100)

        # Humedad del suelo: sube rápido con la bomba y baja despacio sin ella.
        self.hum_suelo += 2.5 if a["bomba"] else -0.25
        self.hum_suelo += random.uniform(-0.05, 0.05)
        self.hum_suelo = limitar(self.hum_suelo, 0, 100)

        # Luz medida: se acerca a la del sol, más 35 si la lámpara está encendida.
        objetivo_luz = self._luz_natural + (35 if a["luz"] else 0)
        self.luz += (objetivo_luz - self.luz) * 0.3 + random.uniform(-0.5, 0.5)
        self.luz = limitar(self.luz, 0, 100)

    def _logica_automatica(self, ahora):
        """Decide qué actuadores encender según los umbrales (igual que el firmware)."""
        u = self.umbrales
        a = self.actuadores

        # Riego: dura TIEMPO_RIEGO segundos y luego espera TIEMPO_ESPERA antes de repetir.
        if a["bomba"] == 1:
            if ahora >= self._fin_riego:
                a["bomba"] = 0
                self._fin_espera = ahora + aj.TIEMPO_ESPERA
        elif self.hum_suelo < u["suelo_min"] and ahora >= self._fin_espera:
            a["bomba"] = 1
            self._fin_riego = ahora + aj.TIEMPO_RIEGO

        # Ventilador: se enciende sobre el máximo y se apaga 2 °C más abajo
        # (así no parpadea cuando la temperatura anda justo en el límite).
        if self.temp > u["temp_max"]:
            a["ventilador"] = 1
        elif self.temp <= u["temp_max"] - 2:
            a["ventilador"] = 0

        # Luz de crecimiento: se decide con la luz del sol, sin contar la propia lámpara.
        a["luz"] = 1 if self._luz_natural < u["luz_min"] else 0

    def _eventos_actuadores(self, antes):
        """Compara el estado de antes con el de ahora y crea un evento por cada cambio."""
        eventos = []
        for nombre, valor in self.actuadores.items():
            if valor != antes[nombre]:
                textos = aj.TEXTO_ACTUADORES[nombre]    # (texto al encender, texto al apagar)
                eventos.append({
                    "evento": textos[0] if valor else textos[1],
                    "valor": "ON" if valor else "OFF",
                    "alerta": False,
                })
        return eventos

    def _revisar_alertas(self):
        """Crea una alerta solo cuando la condición CRUZA el límite, no en cada paso."""
        condiciones = {
            "suelo_seco": (self.hum_suelo < aj.CRIT_SUELO, f"{self.hum_suelo:.0f} %"),
            "temp_alta": (self.temp > aj.CRIT_TEMP, f"{self.temp:.1f} °C"),
        }
        eventos = []
        for tipo, (activa, valor) in condiciones.items():
            if activa and tipo not in self._alertas_activas:
                self._alertas_activas.add(tipo)
                eventos.append({
                    "evento": "ALERTA: " + aj.NOMBRES_ALERTA[tipo],
                    "valor": valor,
                    "alerta": True,
                })
            elif not activa:
                self._alertas_activas.discard(tipo)
        return eventos
