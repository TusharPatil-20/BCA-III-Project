from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import os
import re
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = "my_secret_key_123"

# ------------------------------
# DATABASE CONFIGURATION
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pizza.db")

# ------------------------------
# CREATE DATABASE & TABLE
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            product TEXT,
            price REAL,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# ------------------------------
# SAFE MIGRATION (NO CRASH)
# ------------------------------
def migrate_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("ALTER TABLE orders ADD COLUMN qty INTEGER DEFAULT 1")
    except:
        pass

    try:
        cur.execute("ALTER TABLE orders ADD COLUMN total_price REAL")
    except:
        pass

    conn.commit()
    conn.close()

init_db()
migrate_db()

# ------------------------------
# PUBLIC ROUTES
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/confirm")
def confirm():
    return render_template("confirm.html")

@app.route("/payment")
def payment():

    # 1️⃣ जर URL मधून order आलं असेल तर session मध्ये save कर
    if request.args.get("product"):
        session["last_order"] = {
            "product": request.args.get("product"),
            "price": float(request.args.get("price", 0)),
            "qty": int(request.args.get("qty", 1))
        }

    # 2️⃣ Login नसल्यास → login page
    if not session.get("user"):
        session["next_page"] = url_for("payment")
        return redirect(url_for("user_login"))

    # 3️⃣ Session मधून order घे
    last_order = session.get("last_order")

    # 4️⃣ तरीही order नसेल तर home
    if not last_order:
        return redirect(url_for("home"))

    # 5️⃣ Payment page
    return render_template("payment.html", last_order=last_order)



# ------------------------------
# ADMIN DASHBOARD
# ------------------------------
@app.route("/admin")
def admin():
    if not session.get("admin"):
        session["next_page"] = url_for("admin")
        return redirect(url_for("admin_login"))
    return render_template("admin.html")

# ------------------------------
# USER LOGIN
# ------------------------------
@app.route("/user-login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        phone = request.form.get("phone")

        if not re.fullmatch(r"\d{10}", phone):
            return render_template("user_login.html", error="❌ Invalid phone number")

        next_page = session.pop("next_page", None)
        session.clear()
        session["user"] = phone
        return redirect(next_page or url_for("home"))

    return render_template("user_login.html")

@app.route("/user-logout")
def user_logout():
    session.clear()
    return redirect(url_for("home"))

# ------------------------------
# BOOKING
# ------------------------------
@app.route("/booking")
def booking():
    if not session.get("user"):
        session["next_page"] = url_for("booking")
        return redirect(url_for("user_login"))
    return render_template("booking.html")

# ------------------------------
# PRODUCT DETAILS
# ------------------------------
@app.route("/details-pizza")
def details_pizza():
    return render_template("details-pizza.html")

@app.route("/details-burger")
def details_burger():
    return render_template("details-burger.html")

@app.route("/details-pasta")
def details_pasta():
    return render_template("details-pasta.html")

@app.route("/details-icecream")
def details_icecream():
    return render_template("details-icecream.html")

# ------------------------------
# CATEGORY ROUTES
# ------------------------------
@app.route("/pizza/veg")
def pizza_veg():
    return render_template("pizza/veg.html")

@app.route("/pizza/nonveg")
def pizza_nonveg():
    return render_template("pizza/nonveg.html")

@app.route("/pizza/combo")
def pizza_combo():
    return render_template("pizza/combo.html")

@app.route("/burger/veg")
def burger_veg():
    return render_template("burger/veg.html")

@app.route("/burger/nonveg")
def burger_nonveg():
    return render_template("burger/nonveg.html")

@app.route("/burger/combo")
def burger_combo():
    return render_template("burger/combo.html")

@app.route("/pasta/veg")
def pasta_veg():
    return render_template("pasta/veg.html")

@app.route("/pasta/nonveg")
def pasta_nonveg():
    return render_template("pasta/nonveg.html")

@app.route("/pasta/combo")
def pasta_combo():
    return render_template("pasta/combo.html")

@app.route("/icecream/flavors")
def icecream_flavors():
    return render_template("icecream/flavors.html")

@app.route("/icecream/family")
def icecream_family():
    return render_template("icecream/family.html")

@app.route("/icecream/sundae")
def icecream_sundae():
    return render_template("icecream/sundae.html")

# ------------------------------
# SAVE ORDER (QTY FIXED)
# ------------------------------
@app.route("/save-order", methods=["POST"])
def save_order():

    # ❌ User login नसेल
    if not session.get("user"):
        session["pending_order"] = {
            "customer_name": request.form.get("customer_name"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "product": request.form.get("product"),
            "price": request.form.get("price"),
            "qty": request.form.get("qty"),
        }

        session["next_page"] = url_for("payment")
        return redirect(url_for("user_login"))

    # ✅ User login असेल तर पुढचं logic (DB insert वगैरे)
    # इथे तुझा existing order save code येईल



    data = request.form
    customer = data.get("customer_name")
    phone = data.get("phone")
    address = data.get("address")
    product = data.get("product")
    price = float(data.get("price", 0))
    qty = int(data.get("qty", 1))
    total_price = price * qty
    status = "Cash on Delivery"

    if not all([customer, phone, address, product]):
        return render_template("error.html", message="⚠️ All fields are required!")

    if not re.fullmatch(r"\d{10}", phone):
        return render_template("error.html", message="❌ Invalid phone number")

    ist = pytz.timezone("Asia/Kolkata")
    created_at = datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders
        (customer_name, phone, address, product, price, qty, total_price, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer, phone, address, product,
        price, qty, total_price, status, created_at
    ))
    conn.commit()
    conn.close()

    session["order_success"] = {
        "customer": customer,
        "product": product,
        "price": price,
        "qty": qty,
        "total": total_price
    }

    return redirect(url_for("order_success"))

# ------------------------------
# ORDER SUCCESS
# ------------------------------
@app.route("/order-success")
def order_success():
    data = session.get("order_success")
    if not data:
        return redirect(url_for("home"))

    return render_template(
        "order_success.html",
        customer=data["customer"],
        product=data["product"],
        price=data["price"],
        qty=data["qty"],
        total=data["total"]
    )

# ------------------------------
# ADMIN LOGIN
# ------------------------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        return render_template("admin_login.html", error="❌ Wrong password!")

    return render_template("admin_login.html")

@app.route("/admin-logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

# ------------------------------
# ADMIN ORDERS PAGE
# ------------------------------
@app.route("/orders")
def order_table():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, customer_name, phone, address, product,
               price, qty, total_price, status, created_at
        FROM orders ORDER BY id ASC
    """)
    orders = cur.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)

# ------------------------------
# ADMIN APIs
# ------------------------------
@app.route("/api/orders")
def api_get_orders():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

@app.route("/api/orders/<int:order_id>/toggle", methods=["PATCH"])
def api_toggle_order_status(order_id):
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT status FROM orders WHERE id=?", (order_id,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "Order not found"}), 404

    new_status = "Paid" if row[0] == "Cash on Delivery" else "Cash on Delivery"
    cur.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
def api_delete_order(order_id):
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/api/orders/clear", methods=["DELETE"])
def api_clear_orders():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM orders")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='orders'")
    conn.commit()
    conn.close()

    return jsonify({"success": True})

# ------------------------------
# CONTACT
# ------------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ------------------------------
# RUN APP
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
