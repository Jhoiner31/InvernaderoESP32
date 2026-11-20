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

ACTUADORES = [
    ("bomba", "Bomba de riego"),
    ("ventilador", "Ventilador"),
    ("luz", "Luz de crecimiento"),
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

    #-----------------Tarjetas de sensores-------------
    tarjetas = {}

    for clave, titulo, unidad, maximo, decimales in SENSORES:
        tarjetas[clave] = TarjetaSensor(
            titulo=titulo,
            unidad=unidad,
            maximo=maximo,
            decimales=decimales,
            expand=True,
        )

    # ---------- Interruptores de actuadores ----------
    def cambiar_actuador(e):
        sim.comando(e.control.data, e.control.value)

    switches = {}
    for clave, nombre in ACTUADORES:
        switches[clave] = ft.Switch(
            label=nombre,
            value=False,
            disabled=True,
            data=clave,
            on_change=cambiar_actuador,
        )

    # ---------- Selector de modo ----------
    def cambiar_modo(e):
        modo = e.control.value
        sim.cambiar_modo(modo)
        for sw in switches.values():
            sw.disabled = modo == "auto"
        page.update()

    dd_modo = ft.Dropdown(
        label="Modo",
        value="auto",
        width=180,
        options=[
            ft.DropdownOption(key="auto", text="Automático"),
            ft.DropdownOption(key="manual", text="Manual"),
        ],
        on_select=cambiar_modo,
    )

    # ---------- Distribución ----------
    encabezado = ft.Row(
        controls=[
            ft.Text("Invernadero inteligente", size=22, weight=ft.FontWeight.BOLD),
            dd_modo,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    panel_actuadores = ft.Container(
        bgcolor=paleta["panel"],
        padding=15,
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Text("Actuadores", size=13, color=paleta["tenue"]),
                *switches.values(),
            ],
        ),
    )

    page.add(
        encabezado,
        ft.Row(controls=list(tarjetas.values()), spacing=10),
        panel_actuadores,
    )

    # ---------- Ciclo periódico ----------
    async def ciclo():
        while True:
            paquete = sim.paso()
            if paquete is not None:
                for clave, valor in paquete["sensores"].items():
                    estado = evaluar_estado(clave, valor, umbrales)
                    tarjetas[clave].actualizar(valor, estado)
                for clave, valor in paquete["actuadores"].items():
                    switches[clave].value = bool(valor)
                page.update()
            await asyncio.sleep(aj.INTERVALO_MS / 1000)

    page.run_task(ciclo)

ft.run(main)