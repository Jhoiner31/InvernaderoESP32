import flet as ft
import ajustes as aj
from componentes import TarjetaSensor

colores = aj.COLORES

def evaluar_estado(variable, valor, umbrales):
    if variable == "temp":
        if valor > aj.CRIT_TEMP:
            return "crit"
        if valor > umbrales["temp_max"]:
            return "aviso"
        return "ok"

    if variable == "hum_suelo":
        if valor < aj.CRIT_SUELO:
            return "crit"
        if valor < umbrales["suelo_min"]:
            return "aviso"
        return "ok"

    if variable == "luz":
        if valor < umbrales["luz_min"]:
            return "aviso"
        return "ok"

    # humedad del aire
    if valor < 25 or valor > 90:
        return "crit"
    if valor < 40 or valor > 80:
        return "aviso"
    return "ok"

def indicador(texto, color=None):
    """Circulo de color (LED) + texto."""
    return ft.Row(
        controls=[
            ft.Container(width=12, height=12, border_radius=6,
                         bgcolor=color or colores["tenue"]),
            ft.Text(texto, size=13, color=colores["texto"]),
        ],
        spacing=8,
        tight=True,   # la fila ocupa solo lo necesario, no todo el ancho
    )

def dropdown(opciones):
    """Menu desplegable con la primera opcion seleccionada."""
    return ft.Dropdown(
        label="Modo",
        value=opciones[0],
        width=180,
        border_color=colores["borde"],
        color=colores["tenue"],
        options=[
            ft.DropdownOption(key="auto", text="Automático"),
            ft.DropdownOption(key="manual", text="Manual"),
        ]
    )

def crear_barra_superior():
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Invernadero inteligente", size=20, weight=ft.FontWeight.BOLD,
                        color=colores["texto"]),
                indicador("Broker MQTT: conectado", colores["ok"]),
                indicador("ESP32: esperando datos"),
                ft.Container(expand=True),   # "resorte": empuja lo siguiente a la derecha
                ft.Text("00/00/0000  00:00:00", size=15, color=colores["texto"]),   # reloj
                dropdown(aj.MODOS),
            ],
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=colores["panel"],
        border=ft.Border.only(bottom=ft.BorderSide(1, colores["borde"])),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
    )

def crear_banner():
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("ALERTA: texto de ejemplo", size=15, weight=ft.FontWeight.BOLD,
                        color="white"),
                ft.Container(expand=True),
                ft.TextButton(content="Cerrar", style=ft.ButtonStyle(color="white")),
            ],
        ),
        bgcolor=colores["crit"],
        padding=ft.Padding.symmetric(horizontal=16, vertical=6),
        visible=False,   # True-(Alerta encendida) False-(Alerta apagada)
    )

def crear_monitor():
    #(1) Fila de tarjetas
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