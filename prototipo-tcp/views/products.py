import flet as ft
from database import obtener_productos, registrar_venta, eliminar_producto


def crear_productos(page: ft.Page, on_cambio):

    def cargar():
        productos = obtener_productos()
        items = []
        for p in productos:
            items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(p["nombre"], size=15, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        f"Precio: ${p['precio_venta']:.2f} | Costo: ${p['precio_compra']:.2f}",
                                        size=11,
                                        color=ft.colors.GREY,
                                    ),
                                    ft.Text(
                                        f"Stock: {p['stock']} | Margen: {((p['precio_venta'] - p['precio_compra']) / p['precio_venta'] * 100) if p['precio_venta'] > 0 else 0:.1f}%",
                                        size=11,
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.icons.SHOPPING_CART,
                                tooltip="Vender",
                                on_click=lambda _, pid=p["id"]: _abrir_venta(pid),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                tooltip="Eliminar",
                                icon_color=ft.colors.RED_400,
                                on_click=lambda _, pid=p["id"]: _eliminar(pid),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=12,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=8,
                    margin=ft.margin.only(bottom=6),
                )
            )
        lista_productos.controls = items
        page.update()

    def _eliminar(pid):
        eliminar_producto(pid)
        cargar()
        on_cambio()

    def _abrir_venta(pid):
        from database import obtener_producto

        prod = obtener_producto(pid)
        if not prod:
            return

        txt_cantidad = ft.TextField(
            label="Cantidad",
            keyboard_type=ft.KeyboardType.NUMBER,
            value="1",
            width=100,
        )
        lbl_info = ft.Text(
            f"Producto: {prod['nombre']}\n"
            f"Precio venta: ${prod['precio_venta']:.2f}\n"
            f"Stock disponible: {prod['stock']}",
            size=14,
        )
        lbl_total = ft.Text("Total: $0.00", size=16, weight=ft.FontWeight.BOLD)

        def actualizar_total(e):
            try:
                cant = int(txt_cantidad.value or "0")
                total = cant * prod["precio_venta"]
                lbl_total.value = f"Total: ${total:.2f}"
                page.update()
            except ValueError:
                pass

        txt_cantidad.on_change = actualizar_total

        def confirmar(e):
            try:
                cant = int(txt_cantidad.value or "0")
                if cant <= 0:
                    return
                if cant > prod["stock"]:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Stock insuficiente"),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                ok = registrar_venta(pid, cant)
                if ok:
                    dlg.open = False
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Venta registrada"),
                        bgcolor=ft.colors.GREEN,
                    )
                    page.snack_bar.open = True
                    cargar()
                    on_cambio()
                page.update()
            except ValueError:
                pass

        dlg = ft.AlertDialog(
            title=ft.Text("Registrar Venta"),
            content=ft.Column(
                controls=[lbl_info, txt_cantidad, lbl_total],
                height=150,
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: _cerrar_dialog(dlg)),
                ft.ElevatedButton("Confirmar Venta", on_click=confirmar, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE),
            ],
        )
        page.dialog = dlg
        dlg.open = True
        actualizar_total(None)
        page.update()

    def _cerrar_dialog(dlg):
        dlg.open = False
        page.update()

    lista_productos = ft.Column(scroll=ft.ScrollMode.AUTO)

    vista = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Productos", size=20, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.icons.REFRESH,
                            tooltip="Actualizar",
                            on_click=lambda _: (cargar(), on_cambio()),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=5),
                lista_productos,
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=15,
        expand=True,
    )

    return vista, cargar
