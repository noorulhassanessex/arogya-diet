from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3
import os
from datetime import date, datetime
from functools import wraps

from werkzeug.security import generate_password_hash, check_password_hash

import matplotlib
matplotlib.use("Agg")  # important for saving graphs without GUI
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.secret_key = "CHANGE_THIS_TO_RANDOM_STRING"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
REPORT_DIR = os.path.join(BASE_DIR, "static", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

print("APP DB PATH:", DB_PATH)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


# -------------------------
# DB INIT + SEED FOOD LIST
# -------------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        serving_grams REAL NOT NULL,
        calories REAL NOT NULL,
        protein REAL NOT NULL,
        carbs REAL NOT NULL,
        fat REAL NOT NULL,
        sugar REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS food_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,           -- YYYY-MM-DD
        meal_type TEXT NOT NULL,          -- breakfast/lunch/snack/dinner
        food_item_id INTEGER NOT NULL,
        quantity REAL NOT NULL,           -- servings
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(food_item_id) REFERENCES food_items(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS water_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,
        glasses INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()

    # Seed food items if empty
    cur.execute("SELECT COUNT(*) AS c FROM food_items")
    if cur.fetchone()["c"] == 0:
        seed = [
            ("Special K cereal", 31, 117, 2.4, 23.0, 0.4, 4.0),
            ("Boiled egg", 50, 78, 6.3, 0.6, 5.3, 0.1),
            ("Oats", 40, 150, 5.0, 27.0, 3.0, 1.0),
            ("Milk (semi-skim)", 250, 125, 8.5, 12.0, 4.5, 12.0),
            ("Chicken breast", 100, 165, 31.0, 0.0, 3.6, 0.0),
            ("Rice cooked", 150, 195, 4.0, 42.0, 0.4, 0.1),
            ("Banana", 118, 105, 1.3, 27.0, 0.4, 14.0),
            ("Apple", 182, 95, 0.5, 25.0, 0.3, 19.0),
            ("Greek yogurt", 170, 100, 17.0, 6.0, 0.0, 6.0),
            ("Salmon", 100, 208, 20.0, 0.0, 13.0, 0.0),
            ("Broccoli", 100, 34, 2.8, 7.0, 0.4, 1.7),
            ("Chocolate bar", 45, 235, 2.7, 26.0, 13.0, 24.0),
        ]
        cur.executemany("""
            INSERT INTO food_items (name, serving_grams, calories, protein, carbs, fat, sugar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, seed)
        conn.commit()

    conn.close()


init_db()


# ------------
# AUTH ROUTES
# ------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not email or not password:
            flash("Email and password required.")
            return redirect(url_for("signup"))

        pw_hash = generate_password_hash(password)

        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, pw_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("Email already exists. Try logging in.")
            return redirect(url_for("login"))

        conn.close()
        flash("Account created. Please log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row["password_hash"], password):
            session["user_id"] = row["id"]
            session["email"] = email
            return redirect(url_for("tracker"))

        flash("Invalid email or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ------------
# BASIC PAGES
# ------------
@app.route("/")
def index():
    # If logged in, let them go to tracker
    if "user_id" in session:
        return redirect(url_for("tracker"))
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ------------
# TRACKER
# ------------
@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    user_id = session["user_id"]
    today_str = date.today().isoformat()

    conn = get_conn()
    cur = conn.cursor()

    # dropdown food list
    cur.execute("SELECT id, name FROM food_items ORDER BY name")
    foods = cur.fetchall()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_food":
            meal_type = request.form["meal_type"]
            food_item_id = int(request.form["food_item_id"])
            quantity = float(request.form["quantity"])
            cur.execute("""
                INSERT INTO food_log (user_id, log_date, meal_type, food_item_id, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, today_str, meal_type, food_item_id, quantity))
            conn.commit()

        elif action == "add_water":
            glasses = int(request.form["glasses"])
            cur.execute("""
                INSERT INTO water_log (user_id, log_date, glasses)
                VALUES (?, ?, ?)
            """, (user_id, today_str, glasses))
            conn.commit()

        elif action == "delete_food":
            log_id = int(request.form["log_id"])
            cur.execute("DELETE FROM food_log WHERE id=? AND user_id=?", (log_id, user_id))
            conn.commit()

        elif action == "delete_water":
            water_id = int(request.form["water_id"])
            cur.execute("DELETE FROM water_log WHERE id=? AND user_id=?", (water_id, user_id))
            conn.commit()

    # totals today
    cur.execute("""
        SELECT
          COALESCE(SUM(fi.calories * fl.quantity), 0) as calories,
          COALESCE(SUM(fi.protein  * fl.quantity), 0) as protein,
          COALESCE(SUM(fi.carbs    * fl.quantity), 0) as carbs,
          COALESCE(SUM(fi.fat      * fl.quantity), 0) as fat,
          COALESCE(SUM(fi.sugar    * fl.quantity), 0) as sugar
        FROM food_log fl
        JOIN food_items fi ON fi.id = fl.food_item_id
        WHERE fl.user_id = ? AND fl.log_date = ?
    """, (user_id, today_str))
    totals = cur.fetchone()

    # today food log list
    cur.execute("""
        SELECT fl.id, fl.meal_type, fi.name, fl.quantity,
               ROUND(fi.calories*fl.quantity, 1) as calories
        FROM food_log fl
        JOIN food_items fi ON fi.id = fl.food_item_id
        WHERE fl.user_id=? AND fl.log_date=?
        ORDER BY fl.created_at DESC
    """, (user_id, today_str))
    today_food = cur.fetchall()

    # water today + list
    cur.execute("""
        SELECT id, glasses, log_date FROM water_log
        WHERE user_id=? AND log_date=?
        ORDER BY created_at DESC
    """, (user_id, today_str))
    water_rows = cur.fetchall()

    cur.execute("SELECT COALESCE(SUM(glasses), 0) AS total FROM water_log WHERE user_id=? AND log_date=?",
                (user_id, today_str))
    water_total = cur.fetchone()["total"]

    conn.close()

    return render_template(
        "tracker.html",
        today=today_str,
        email=session.get("email"),
        foods=foods,
        today_food=today_food,
        water_rows=water_rows,
        water_total=water_total,
        totals=totals
    )


# ------------
# BMI (unchanged logic, protected)
# ------------
@app.route("/bmi", methods=["GET", "POST"])
@login_required
def bmi():
    bmi_value = None
    category = None
    suggested_plans = []

    if request.method == "POST":
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height")) / 100

        bmi_value = round(weight / (height * height), 2)

        if bmi_value < 18.5:
            category = "Underweight"
            suggested_plans = ["High-Protein Gain Plan", "Balanced Diet Plan"]
        elif bmi_value < 25:
            category = "Healthy"
            suggested_plans = ["Balanced Diet Plan"]
        elif bmi_value < 30:
            category = "Overweight"
            suggested_plans = ["Weight Loss Plan", "Low-Carb Plan"]
        else:
            category = "Obese"
            suggested_plans = ["Weight Loss Plan", "Low-Carb Plan"]

    return render_template("bmi.html", bmi=bmi_value, category=category, suggested_plans=suggested_plans)


# ------------
# MEAL PLAN (unchanged)
# ------------
@app.route("/meal-plan")
@login_required
def meal_plan():
    plan_name = request.args.get("name")

    plans = {
        "High-Protein Gain Plan": [
            "Breakfast: Eggs + Oats + Milk",
            "Lunch: Chicken + Rice + Vegetables",
            "Dinner: Fish + Sweet Potatoes"
        ],
        "Balanced Diet Plan": [
            "Breakfast: Oats + Fruits",
            "Lunch: Rice + Vegetables",
            "Dinner: Grilled Fish"
        ],
        "Weight Loss Plan": [
            "Breakfast: Boiled Eggs",
            "Lunch: Chicken Salad",
            "Dinner: Vegetable Soup"
        ],
        "Low-Carb Plan": [
            "Breakfast: Greek Yogurt",
            "Lunch: Chicken + Broccoli",
            "Dinner: Salmon + Spinach"
        ]
    }

    items = plans.get(plan_name)
    return render_template("meal_plan.html", name=plan_name, items=items)


# ------------
# REPORT (date range + averages + graph + warning)
# ------------
@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    user_id = session["user_id"]
    today = date.today().isoformat()

    start = request.values.get("start_date") or today
    end = request.values.get("end_date") or today

    conn = get_conn()
    cur = conn.cursor()

    # daily totals for range
    cur.execute("""
    SELECT log_date,
           ROUND(SUM(fi.calories*fl.quantity),1) AS calories,
           ROUND(SUM(fi.protein*fl.quantity),1)  AS protein,
           ROUND(SUM(fi.carbs*fl.quantity),1)    AS carbs,
           ROUND(SUM(fi.fat*fl.quantity),1)      AS fat,
           ROUND(SUM(fi.sugar*fl.quantity),1)    AS sugar
    FROM food_log fl
    JOIN food_items fi ON fi.id = fl.food_item_id
    WHERE fl.user_id=? AND fl.log_date BETWEEN ? AND ?
    GROUP BY log_date
    ORDER BY log_date
    """, (user_id, start, end))
    daily = cur.fetchall()

    # compute averages
    n_days = len(daily)
    sums = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}
    for r in daily:
        sums["calories"] += r["calories"] or 0
        sums["protein"] += r["protein"] or 0
        sums["carbs"] += r["carbs"] or 0
        sums["fat"] += r["fat"] or 0
        sums["sugar"] += r["sugar"] or 0

    avgs = {k: (sums[k] / n_days if n_days else 0) for k in sums}

    # Build a calories trend warning (simple linear projection)
    warning = None
    target_calories = 1500  # change if you want
    if n_days >= 4:
        # x = 0..n-1, y = calories
        x = list(range(n_days))
        y = [r["calories"] or 0 for r in daily]
        # simple linear fit using polyfit (no numpy requirement)
        # We'll implement quick least squares:
        x_mean = sum(x) / n_days
        y_mean = sum(y) / n_days
        denom = sum((xi - x_mean) ** 2 for xi in x)
        slope = (sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n_days)) / denom) if denom else 0
        intercept = y_mean - slope * x_mean

        # predict next 7 days
        will_exceed = False
        for future in range(n_days, n_days + 7):
            pred = slope * future + intercept
            if pred > target_calories:
                will_exceed = True
                break
        if will_exceed:
            warning = f"Early warning: calorie trend may exceed {target_calories} kcal/day soon."

    # Create graph (calories over time)
    graph_file = None
    if n_days >= 1:
        dates = [r["log_date"] for r in daily]
        cals = [r["calories"] for r in daily]
        plt.figure()
        plt.plot(dates, cals, marker="o")
        plt.xticks(rotation=45, ha="right")
        plt.title("Calories Over Time")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.tight_layout()

        graph_file = f"calories_{user_id}_{start}_to_{end}.png".replace(":", "_")
        graph_path = os.path.join(REPORT_DIR, graph_file)
        plt.savefig(graph_path, dpi=150)
        plt.close()

    conn.close()

    return render_template(
        "report.html",
        start_date=start,
        end_date=end,
        daily=daily,
        avgs=avgs,
        warning=warning,
        graph_file=graph_file
    )


# ------------
# PDF EXPORT
# ------------
@app.route("/report/pdf")
@login_required
def report_pdf():
    user_id = session["user_id"]
    email = session.get("email", "user")
    today = date.today().isoformat()

    start = request.args.get("start") or today
    end = request.args.get("end") or today

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT log_date,
           ROUND(SUM(fi.calories*fl.quantity),1) AS calories,
           ROUND(SUM(fi.protein*fl.quantity),1)  AS protein,
           ROUND(SUM(fi.carbs*fl.quantity),1)    AS carbs,
           ROUND(SUM(fi.fat*fl.quantity),1)      AS fat,
           ROUND(SUM(fi.sugar*fl.quantity),1)    AS sugar
    FROM food_log fl
    JOIN food_items fi ON fi.id = fl.food_item_id
    WHERE fl.user_id=? AND fl.log_date BETWEEN ? AND ?
    GROUP BY log_date
    ORDER BY log_date
    """, (user_id, start, end))
    daily = cur.fetchall()
    conn.close()

    # calculate averages
    n_days = len(daily)
    sums = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}
    for r in daily:
        for k in sums:
            sums[k] += (r[k] or 0)
    avgs = {k: (sums[k] / n_days if n_days else 0) for k in sums}

    pdf_name = f"arogya_report_{user_id}_{start}_to_{end}.pdf".replace(":", "_")
    pdf_path = os.path.join(BASE_DIR, pdf_name)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Arogya Diet Report")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"User: {email}")
    y -= 15
    c.drawString(50, y, f"Date range: {start} to {end}")
    y -= 25

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Average daily intake")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Calories: {avgs['calories']:.1f} kcal/day")
    y -= 14
    c.drawString(50, y, f"Protein: {avgs['protein']:.1f} g/day")
    y -= 14
    c.drawString(50, y, f"Carbs: {avgs['carbs']:.1f} g/day")
    y -= 14
    c.drawString(50, y, f"Fat: {avgs['fat']:.1f} g/day")
    y -= 14
    c.drawString(50, y, f"Sugar: {avgs['sugar']:.1f} g/day")
    y -= 22

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Daily breakdown")
    y -= 18

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Date")
    c.drawString(120, y, "Cal")
    c.drawString(170, y, "Prot")
    c.drawString(220, y, "Carb")
    c.drawString(270, y, "Fat")
    c.drawString(320, y, "Sugar")
    y -= 12
    c.setFont("Helvetica", 9)

    for r in daily:
        if y < 80:
            c.showPage()
            y = height - 50
        c.drawString(50, y, r["log_date"])
        c.drawString(120, y, str(r["calories"]))
        c.drawString(170, y, str(r["protein"]))
        c.drawString(220, y, str(r["carbs"]))
        c.drawString(270, y, str(r["fat"]))
        c.drawString(320, y, str(r["sugar"]))
        y -= 12

    c.showPage()
    c.save()

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)