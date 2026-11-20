import flet as ft
import ajustes as aj

@ft.control
class TarjetaSensor(ft.Container):
    titulo: str = ""
    unidad: str = ""
    maximo: float = 100
    decimales: int = 0

    def init(self):
        paleta = aj.PALETAS["oscuro"]

        self.lbl_valor = ft.Text("--", size=28, weight=ft.FontWeight.BOLD)
        self.barra = ft.ProgressBar(value=0, color=paleta["ok"], bgcolor=paleta["borde"])

        self.bgcolor = paleta["panel"]
        self.padding = 15
        self.border_radius = 10
        self.content = ft.Column(
            controls = [
                ft.Text(self.titulo, size=13, color=paleta["tenue"]),
                self.lbl_valor,
                self.barra
            ]
        )

    def actualizar(self, nuevo, estado):
        paleta = aj.PALETAS["oscuro"]
        color = paleta[estado]

        self.lbl_valor.value = f"{nuevo:.{self.decimales}f} {self.unidad}"
        self.barra.value = max(0, min(1, nuevo / self.maximo))
        self.barra.color = color

        self.update()