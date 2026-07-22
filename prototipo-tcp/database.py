import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def iniciar_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio_compra REAL NOT NULL DEFAULT 0,
            precio_venta REAL NOT NULL DEFAULT 0,
            stock INTEGER NOT NULL DEFAULT 0,
            creado_en TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL REFERENCES productos(id),
            cantidad INTEGER NOT NULL,
            total_venta REAL NOT NULL,
            total_costo REAL NOT NULL,
            ganancia REAL NOT NULL,
            creado_en TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        );
    """)
    conn.commit()
    conn.close()


def agregar_producto(nombre, precio_compra, precio_venta, stock):
    conn = get_connection()
    conn.execute(
        "INSERT INTO productos (nombre, precio_compra, precio_venta, stock) VALUES (?, ?, ?, ?)",
        (nombre, precio_compra, precio_venta, stock),
    )
    conn.commit()
    conn.close()


def eliminar_producto(producto_id):
    conn = get_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()


def obtener_productos():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM productos ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def obtener_producto(producto_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def registrar_venta(producto_id, cantidad):
    producto = obtener_producto(producto_id)
    if not producto:
        return False
    if producto["stock"] < cantidad:
        return False

    total_venta = round(cantidad * producto["precio_venta"], 2)
    total_costo = round(cantidad * producto["precio_compra"], 2)
    ganancia = round(total_venta - total_costo, 2)

    conn = get_connection()
    conn.execute(
        "INSERT INTO ventas (producto_id, cantidad, total_venta, total_costo, ganancia) VALUES (?, ?, ?, ?, ?)",
        (producto_id, cantidad, total_venta, total_costo, ganancia),
    )
    conn.execute(
        "UPDATE productos SET stock = stock - ? WHERE id = ?",
        (cantidad, producto_id),
    )
    conn.commit()
    conn.close()
    return True


def resumen_dia(fecha=None):
    if fecha is None:
        fecha = date.today().isoformat()
    conn = get_connection()
    row = conn.execute(
        """
        SELECT
            COALESCE(SUM(total_venta), 0) as total_vendido,
            COALESCE(SUM(total_costo), 0) as total_costo,
            COALESCE(SUM(ganancia), 0) as ganancia_total,
            COUNT(*) as cantidad_ventas
        FROM ventas
        WHERE date(creado_en) = ?
        """,
        (fecha,),
    ).fetchone()
    conn.close()
    return dict(row)


def ventas_recientes(limite=10):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT v.*, p.nombre as producto_nombre
        FROM ventas v
        JOIN productos p ON p.id = v.producto_id
        ORDER BY v.creado_en DESC
        LIMIT ?
        """,
        (limite,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def productos_stock_bajo(limite=5):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM productos WHERE stock <= ? ORDER BY stock ASC",
        (limite,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
