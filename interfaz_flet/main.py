import flet as ft
import ajustes as aj
from componentes import TarjetaSensor

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

    temp = TarjetaSensor(titulo="Temperatura", unidad= "°C", maximo=50, decimales=1, expand=True)
    luz = TarjetaSensor(titulo="Luz ambiente", unidad= "%", expand=True)
    hum_aire = TarjetaSensor(titulo="Humedad del aire", unidad= "%", expand=True)
    hum_suelo = TarjetaSensor(titulo="Humedad del suelo", unidad= "%", expand=True)

    page.add(ft.Row(controls=[temp, hum_aire, hum_suelo, luz], spacing=10))

    temp.actualizar(50, "crit")

ft.run(main)