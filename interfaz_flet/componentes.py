import flet as ft
import ajustes as aj

colores = aj.COLORES

@ft.control
class TarjetaSensor(ft.Container):
    titulo: str = ""
    unidad: str = ""
    maximo: float = 100
    decimales: int = 0
    estado: str = ""

    def init(self):
        self.lbl_valor = ft.Text("--", size=28, weight=ft.FontWeight.BOLD)
        self.barra = ft.ProgressBar(value=0, color=colores[self.estado], bgcolor=colores["borde"])
        self.indicador_estd = ft.Text(self.estado, size=15, weight=ft.FontWeight.BOLD, color=colores[self.estado])

        self.bgcolor = colores["panel"]
        self.padding = 15
        self.border_radius = 10

        self.content = ft.Column(
            controls = [
                ft.Text(self.titulo, size=13, color=colores["tenue"]),
                self.lbl_valor,
                self.barra,
                self.indicador_estd
            ]
        )

    def actualizar(self, nuevo, estado):
        color = colores[estado]

        self.lbl_valor.value = f"{nuevo:.{self.decimales}f} {self.unidad}"
        self.barra.value = max(0, min(1, nuevo / self.maximo))
        self.barra.color = color

        self.update()