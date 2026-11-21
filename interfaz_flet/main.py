from funciones import *
from componentes import TarjetaSensor

colores = aj.COLORES
sensores = aj.SENSORES
actuadores = aj.ACTUADORES

def main(page: ft.Page):
    page.title = "Invernadero inteligente - Panel de control"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(font_family=aj.FUENTE)
    page.bgcolor = colores["fondo"]
    page.padding = 0
    page.window.width = 1260
    page.window.height = 820
    page.window.min_width = 1100
    page.window.min_height = 760

    #-----------------Tarjetas de sensores-------------
    tarjetas = {}

    for clave, titulo, unidad, maximo, decimales, estado in sensores:
        tarjetas[clave] = TarjetaSensor(
            titulo=titulo,
            unidad=unidad,
            maximo=maximo,
            decimales=decimales,
            estado=estado,
            expand=True,
        )

    pestanas = ft.Tabs(
        length=2,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.TabBar(tabs=[ft.Tab(label="Monitor"), ft.Tab(label="Historial")]),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(content=crear_monitor(), padding=10),
                    ],
                ),
            ],
        ),
    )

    page.add(
        ft.Column(
            controls=[crear_barra_superior(), crear_banner(), pestanas],
            spacing=0,
            expand=True,
        )
    )

ft.run(main)