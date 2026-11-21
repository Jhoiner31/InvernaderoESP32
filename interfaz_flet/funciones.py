import flet as ft

import ajustes as aj
from componentes import caja, dibujar_graficas, TarjetaSensor, dropdown, tabla

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
                dropdown("Modos", aj.MODOS, 180),
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

def crear_actuadores():
    filas = []
    for clave , etiqueta in aj.ACTUADORES:
        filas.append(
            ft.Row(
                controls = [
                    indicador(etiqueta),
                    ft.Container(expand=True),
                    ft.Switch(value=False, disabled=True, active_color=colores["ok"]),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    filas.append(ft.Text("Interruptores disponibles solo en modo manual",
                         size=11, color=colores["tenue"]))
    return caja("Actuadores", ft.Column(controls=filas, spacing=4))

def crear_umbrales():
    controles = []
    for clave, nombre, unidad, minimo, maximo in aj.UMBRALES_CAMPOS:
        valor = aj.UMBRALES_INICIALES[clave]
        controles.append(ft.Text(f"{nombre} ({unidad})", size=12, color=colores["texto"]))
        controles.append(
            ft.Row(
                controls=[
                    ft.Slider(min=minimo, max=maximo, value=valor,
                              divisions=maximo - minimo, expand=True,
                              active_color=colores["acento"]),
                    ft.TextField(value=str(valor), width=64, text_align=ft.TextAlign.CENTER,
                                 text_size=13, dense=True, bgcolor=colores["fondo"],
                                 border_color=colores["borde"]),
                ],
                spacing=4,
            )
        )
    controles.append(ft.Text("", size=11, color=colores["crit"]))   # mensaje de error (vacio)
    controles.append(
        ft.Row(controls=[ft.Button(content="Aplicar", bgcolor=colores["acento"],
                                           color="white", expand=True)])
    )
    return caja("Umbrales del modo automático", ft.Column(controls=controles, spacing=2))

def crear_monitor():
    # (1) Fila de tarjetas
    sensores = aj.SENSORES
    tarjetas_sensor = {}

    for clave, titulo, unidad, maximo, decimales, estado in sensores:
        tarjetas_sensor[clave] = TarjetaSensor(
            titulo=titulo,
            unidad=unidad,
            maximo=maximo,
            decimales=decimales,
            estado=estado,
            expand=True,
        )

    tarjetas = dict(tarjetas_sensor)
    tarjetas = list(tarjetas.values())

    tarjetas = ft.Row(
        controls=tarjetas,
        spacing=10,
    )

    # (2) Grafica con sus dos menus
    grafica = caja(
        "Grafica en tiempo real",
        ft.Column(
            controls = [
                ft.Row(controls = [
                    dropdown("Variable", aj.VARIABLES, 245),
                    dropdown("Rango", aj.RANGOS, 110),
                ]),
                dibujar_graficas()
            ],
            expand = True,
        ),
        expand = 3
    )

    # (3) Registro de eventos
    eventos = caja(
        "Registro de eventos",
        tabla(["Fecha y hora", "Evento", "Valor"]),
        expand =1
    )

    columna_izquierda = ft.Column(controls=[tarjetas, grafica, eventos],
                                  spacing=10, expand=True)

    panel_derecho = ft.Container(
        content = ft.Column(controls=[crear_actuadores(), crear_umbrales()], spacing=10, scroll=ft.ScrollMode.AUTO),
        width = 330
    )


    return ft.Row(
        controls=[columna_izquierda, panel_derecho],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

