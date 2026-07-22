import flet as ft
from database import iniciar_db
from views.home import crear_home
from views.products import crear_productos
from views.add_product import mostrar_agregar_producto


def main(page: ft.Page):
    page.title = "GestiónPro TCP"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_900

    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.TEAL,
        use_material3=True,
    )

    iniciar_db()

    home_view, cargar_home = crear_home(page)
    products_view, cargar_productos = crear_productos(page, recargar_todo)

    contenedor = ft.Container(content=home_view, expand=True)

    indice_actual = 0

    def recargar_todo():
        cargar_home()
        cargar_productos()

    def cambiar_vista(e):
        nonlocal indice_actual
        idx = e.control.selected_index
        if idx == indice_actual:
            return
        indice_actual = idx
        if idx == 0:
            contenedor.content = home_view
            cargar_home()
        elif idx == 1:
            contenedor.content = products_view
            cargar_productos()
        page.update()

    def abrir_agregar(e):
        mostrar_agregar_producto(page, recargar_todo)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click=abrir_agregar,
        bgcolor=ft.Colors.TEAL,
        foreground_color=ft.Colors.WHITE,
    )

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=cambiar_vista,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Inicio"),
            ft.NavigationDestination(icon=ft.icons.INVENTORY_OUTLINED, selected_icon=ft.icons.INVENTORY, label="Productos"),
        ],
    )

    page.add(contenedor)
    cargar_home()


if __name__ == "__main__":
    ft.app(target=main)
