import sqlite3
from datetime import datetime

DB_NAME = "pizza.db"

# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Orders table (FINAL STRUCTURE)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            product TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'Placed',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------
# ADD NEW ORDER
# -----------------------------------
def add_order(data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    total_price = data["price"] * data["qty"]

    cur.execute("""
        INSERT INTO orders
        (customer_name, phone, address, product, price, qty, total_price, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["customer_name"],
        data.get("phone"),
        data.get("address"),
        data["product"],
        data["price"],
        data["qty"],
        total_price,
        "Placed",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# -----------------------------------
# GET ALL ORDERS
# -----------------------------------
def get_orders():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, customer_name, phone, address, product,
               price, qty, total_price, status, created_at
        FROM orders
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


# -----------------------------------
# DELETE SINGLE ORDER
# -----------------------------------
def delete_order(order_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()


# -----------------------------------
# CLEAR ALL ORDERS + RESET ID
# -----------------------------------
def clear_orders_and_reset_id():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM orders")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
    conn.commit()
    conn.close()


# -----------------------------------
# TOGGLE STATUS
# -----------------------------------
def toggle_status(order_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()

    if row:
        new_status = "Completed" if row[0] == "Placed" else "Placed"
        cur.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))

    conn.commit()
    conn.close()
