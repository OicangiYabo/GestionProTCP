import flet as ft
from database import agregar_producto


def mostrar_agregar_producto(page: ft.Page, on_confirmado):
    txt_nombre = ft.TextField(label="Nombre del producto", autofocus=True, expand=True)
    txt_precio_compra = ft.TextField(
        label="Precio de compra",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=140,
    )
    txt_precio_venta = ft.TextField(
        label="Precio de venta",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=140,
    )
    txt_stock = ft.TextField(
        label="Stock inicial",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=100,
        value="0",
    )

    def guardar(e):
        nombre = txt_nombre.value.strip()
        if not nombre:
            page.snack_bar = ft.SnackBar(content=ft.Text("El nombre es obligatorio"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            precio_compra = float(txt_precio_compra.value or "0")
            precio_venta = float(txt_precio_venta.value or "0")
            stock = int(txt_stock.value or "0")
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Verifica los valores numéricos"))
            page.snack_bar.open = True
            page.update()
            return

        agregar_producto(nombre, precio_compra, precio_venta, stock)
        dlg.open = False
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"'{nombre}' agregado"),
            bgcolor=ft.Colors.GREEN,
        )
        page.snack_bar.open = True
        on_confirmado()
        page.update()

    def cancelar(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Nuevo Producto"),
        content=ft.Column(
            controls=[
                txt_nombre,
                ft.Row(controls=[txt_precio_compra, txt_precio_venta]),
                txt_stock,
            ],
            height=200,
            tight=True,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.ElevatedButton("Guardar", on_click=guardar),
        ],
    )
    page.dialog = dlg
    dlg.open = True
    page.update()
