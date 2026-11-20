import flet as ft
import ajustes as aj
import asyncio

from componentes import TarjetaSensor
from logica import evaluar_estado
from simulador import Simulador

SENSORES = [
    ("temp", "Temperatura", "°C", 50, 1),
    ("hum_aire", "Humedad del aire", "%", 100, 0),
    ("hum_suelo", "Humedad del suelo", "%", 100, 0),
    ("luz", "Luz ambiente", "%", 100, 0),
]

def main(page: ft.Page):
    paleta = aj.PALETAS["oscuro"]
    page.title = "Invernadero inteligente"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = paleta["fondo"]
    page.padding = 20
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 900
    page.window.min_height = 650

    sim = Simulador()
    umbrales = dict(aj.UMBRALES_INICIALES)

    tarjetas = {}

    for clave, titulo, unidad, maximo, decimales in SENSORES:
        tarjetas[clave] = TarjetaSensor(
            titulo=titulo,
            unidad=unidad,
            maximo=maximo,
            decimales=decimales,
            expand=True,
        )

    page.add(ft.Row(controls=list(tarjetas.values()), spacing=10))

    async def ciclo():
        while True:
            paquete = sim.paso()
            if paquete is not None:
                for clave, valor in paquete["sensores"].items():
                    estado = evaluar_estado(clave, valor, umbrales)
                    tarjetas[clave].actualizar(valor, estado)
            await asyncio.sleep(aj.INTERVALO_MS / 1000)

    page.run_task(ciclo)

ft.run(main)