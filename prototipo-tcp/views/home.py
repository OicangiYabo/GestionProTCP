import flet as ft
from database import resumen_dia, ventas_recientes, productos_stock_bajo
from datetime import date


def crear_home(page: ft.Page):
    fecha_hoy = date.today()

    def cargar_datos():
        resumen = resumen_dia(fecha_hoy.isoformat())
        ventas = ventas_recientes(5)
        stock_bajo = productos_stock_bajo()

        txt_vendido.value = f"${resumen['total_vendido']:.2f}"
        txt_ganancia.value = f"${resumen['ganancia_total']:.2f}"
        txt_ventas.value = str(resumen["cantidad_ventas"])

        filas_ventas = []
        for v in ventas:
            filas_ventas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(v["producto_nombre"], size=12)),
                        ft.DataCell(ft.Text(str(v["cantidad"]), size=12)),
                        ft.DataCell(ft.Text(f"${v['total_venta']:.2f}", size=12)),
                        ft.DataCell(ft.Text(f"${v['ganancia']:.2f}", size=12)),
                    ]
                )
            )
        tabla_ventas.rows = filas_ventas

        items_bajo = []
        for p in stock_bajo:
            items_bajo.append(
                ft.ListTile(
                    title=ft.Text(p["nombre"], size=13),
                    subtitle=ft.Text(f"Stock: {p['stock']} unidades", size=11),
                    trailing=ft.Icon(ft.icons.WARNING_AMBER, color=ft.colors.ORANGE),
                )
            )
        if not items_bajo:
            items_bajo.append(
                ft.ListTile(title=ft.Text("No hay productos con stock bajo", size=13))
            )
        lista_bajo.controls = items_bajo

        page.update()

    txt_vendido = ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)
    txt_ganancia = ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    txt_ventas = ft.Text("0", size=24, weight=ft.FontWeight.BOLD)

    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cant")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Ganancia")),
        ],
        rows=[],
        column_spacing=20,
        heading_row_height=30,
        data_row_min_height=30,
    )

    lista_bajo = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)

    vista = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Resumen del día", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=5),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Vendido", size=12, color=ft.colors.GREY),
                                    txt_vendido,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            col={"sm": 4},
                            padding=10,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Ganancia", size=12, color=ft.colors.GREY),
                                    txt_ganancia,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            col={"sm": 4},
                            padding=10,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Ventas", size=12, color=ft.colors.GREY),
                                    txt_ventas,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            col={"sm": 4},
                            padding=10,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10,
                        ),
                    ],
                ),
                ft.Divider(height=15),
                ft.Text("Últimas ventas", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column(
                        controls=[tabla_ventas],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=180,
                ),
                ft.Divider(height=15),
                ft.Text("Stock bajo", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=lista_bajo,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=8,
                    padding=5,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=15,
        expand=True,
    )

    return vista, cargar_datos
