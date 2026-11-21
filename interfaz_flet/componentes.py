import flet as ft
import flet_charts as fch
import ajustes as aj

colores = aj.COLORES
texto_estado = aj.TEXTO_ESTADO

@ft.control
class TarjetaSensor(ft.Container):
    titulo: str = ""
    unidad: str = ""
    maximo: float = 100
    decimales: int = 0
    estado: str = ""

    def init(self):
        self.lbl_valor = ft.Text("--", size=30, weight=ft.FontWeight.BOLD, color=colores["texto"])
        self.barra = ft.ProgressBar(value=0, color=colores[self.estado], bgcolor=colores["borde"])
        self.indicador_estd = ft.Text(texto_estado[self.estado], size=13, weight=ft.FontWeight.BOLD, color=colores[self.estado])
        self.franja_sup = ft.Container(height=4, bgcolor=colores[self.estado])

        self.bgcolor = colores["panel"]
        self.border_radius = 8

        self.content = ft.Column(controls=[
            ft.Column(controls=[self.franja_sup]),
            ft.Container(ft.Column(
            controls = [
                ft.Text(self.titulo, size=13, color=colores["tenue"]),
                self.lbl_valor,
                self.barra,
                self.indicador_estd
            ],
            spacing=8,
            ),
            padding=ft.Padding.only(left=12, right=12, bottom=10))
        ],
        spacing=0)

    def actualizar(self, nuevo, estado):
        color = colores[estado]

        self.lbl_valor.value = f"{nuevo:.{self.decimales}f} {self.unidad}"
        self.barra.value = max(0, min(1, nuevo / self.maximo))
        self.barra.color = color
        self.indicador_estd.color = color
        self.franja_sup.bgcolor = color

        self.update()

def dropdown(titulo ,opciones, ancho):
    """Menu desplegable con la primera opcion seleccionada."""
    return ft.Dropdown(
        label=titulo,
        value=opciones[0],
        width=ancho,
        border_color=colores["borde"],
        color=colores["tenue"],
        options=[
            ft.DropdownOption(key=o, text=o) for o in opciones
        ]
    )

def caja(titulo, contenido, expand=False):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(titulo, size=13, weight=ft.FontWeight.BOLD, color=colores["texto"]),
                contenido,
            ],
            spacing = 20,
            expand = bool(expand),
        ),
        bgcolor=colores["panel"],
        border_radius=8,
        padding=12,
        expand = expand,
    )

def dibujar_graficas():
    N_PUNTOS = 20
    COLORES = [ft.Colors.BLUE, ft.Colors.RED, ft.Colors.GREEN, ft.Colors.ORANGE]
    sensores = aj.VARIABLES

    series = [
        fch.LineChartData(
            points=[fch.LineChartDataPoint(x, 0) for x in range(N_PUNTOS)],
            color=COLORES[i],
            stroke_width=3,
            curved=True,
        )
        for i in range(len(sensores))
    ]

    graficas = fch.LineChart(
        data_series=series,
        min_x=0, max_x=N_PUNTOS - 1,
        min_y=0, max_y=100,
        expand=True,
        left_axis=fch.ChartAxis(
            title=ft.Text("Temperatura (C)", color=colores["tenue"]),
            title_size=30,
            label_size=40,
            label_spacing=10
        ),
        bottom_axis=fch.ChartAxis(
            title=ft.Text("Medicion", color=colores["tenue"]),
            title_size=30,
            label_size=40,
            label_spacing=1
        ),
        horizontal_grid_lines=fch.ChartGridLines(
            interval=10,
            color=colores["tenue"],
            width=1
        ),
        vertical_grid_lines=fch.ChartGridLines(
            interval=1,
            color=colores["tenue"],
            width=1
        ),
    )
    return graficas

def tabla(columnas):
    data_table = ft.DataTable(
        columns = [ft.DataColumn(ft.Text(titulo, size=13, color=colores["texto"], weight=ft.FontWeight.BOLD)) for titulo in columnas],
        rows = [],
        heading_row_color=colores["borde"],
        data_row_min_height=28,
        column_spacing=30,
    )
    return ft.Column(controls=[data_table], scroll=ft.ScrollMode.AUTO, expand=True)