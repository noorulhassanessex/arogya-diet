from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# -----------------------------------
# DATABASE INITIALIZATION
# -----------------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT,
            calories INTEGER,
            date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS water (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            glasses INTEGER,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------------
# ROUTES
# -----------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tracker")
def tracker():
    return render_template("tracker.html")


# -----------------------------------
# BMI CALCULATOR (ONLY ONE!)
# -----------------------------------
@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    bmi_value = None
    category = None
    suggested_plans = []

    if request.method == "POST":
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height")) / 100  # cm → meters

        bmi_value = round(weight / (height * height), 2)

        if bmi_value < 18.5:
            category = "Underweight"
            suggested_plans = [
                "High-Protein Gain Plan",
                "Balanced Diet Plan"
            ]
        elif bmi_value < 25:
            category = "Healthy"
            suggested_plans = ["Balanced Diet Plan"]
        elif bmi_value < 30:
            category = "Overweight"
            suggested_plans = [
                "Weight Loss Plan",
                "Low-Carb Plan"
            ]
        else:
            category = "Obese"
            suggested_plans = [
                "Weight Loss Plan",
                "Low-Carb Plan"
            ]

    return render_template(
        "bmi.html",
        bmi=bmi_value,
        category=category,
        suggested_plans=suggested_plans
    )


# -----------------------------------
# MEAL PLAN PAGE
# -----------------------------------
@app.route("/meal_plan")
def meal_plan():
    plan_name = request.args.get("name")
    plans = {
        "High-Protein Gain Plan": [
        "Breakfast: Eggs + Oats + Milk",
        "Snack: Greek yogurt + Banana",
        "Lunch: Chicken + Rice + Vegetables",
        "Snack: Nuts + Fruit",
        "Dinner: Fish + Sweet Potatoes"
       ],
       "Balanced Diet Plan": [
        "Breakfast: Oats + Fruits",
        "Snack: Apple + Peanut butter",
        "Lunch: Rice + Vegetables + Yogurt",
        "Snack: Smoothie (milk + banana)",
        "Dinner: Grilled Fish + Salad"
       ],
        "Weight Loss Plan": [
        "Breakfast: Boiled Eggs + Green tea",
        "Snack: Fruit bowl",
        "Lunch: Chicken Salad",
        "Snack: Greek yogurt",
        "Dinner: Vegetable Soup"
       ],
       "Low-Carb Plan": [
        "Breakfast: Greek Yogurt + Nuts",
        "Snack: Boiled egg",
        "Lunch: Chicken + Broccoli",
        "Snack: Cucumber + hummus",
        "Dinner: Salmon + Spinach"
       ],

       # ✅ NEW PLANS
       "Vegetarian Plan": [
        "Breakfast: Oats + Milk + Banana",
        "Snack: Mixed nuts",
        "Lunch: Lentils (daal) + Brown rice + Salad",
        "Snack: Yogurt + berries",
        "Dinner: Vegetable curry + Roti"
        ],
       "Keto Plan": [
        "Breakfast: Omelette + avocado",
        "Snack: Nuts",
        "Lunch: Chicken salad (olive oil)",
        "Snack: Cheese cubes",
        "Dinner: Salmon + greens"
        ],
        "Muscle Building Plan": [
        "Breakfast: Eggs + Peanut butter toast",
        "Snack: Protein smoothie",
        "Lunch: Chicken + Rice + Veg",
        "Snack: Greek yogurt + banana",
        "Dinner: Beef/Fish + Potatoes"
        ],
        "Diabetic-Friendly Plan": [
        "Breakfast: Oats + nuts (no sugar)",
        "Snack: Apple",
        "Lunch: Grilled chicken + salad",
        "Snack: Yogurt (unsweetened)",
        "Dinner: Vegetable soup + beans"
       ]
    }

    items = plans.get(plan_name)

    return render_template(
        "meal_plan.html",
        name=plan_name,
        items=items
    ) 
@app.route("/report", methods=["GET"])
def report():
    # default: last 7 days
    end = request.args.get("end_date") or date.today().isoformat()
    start = request.args.get("start_date")
    if not start:
        start = (date.fromisoformat(end) - timedelta(days=6)).isoformat()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # meals per day
    cur.execute("""
        SELECT date as log_date,
               SUM(calories) as calories
        FROM meals
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date
    """, (start, end))
    rows = cur.fetchall()

    # water per day
    cur.execute("""
        SELECT date as log_date,
               SUM(glasses) as glasses
        FROM water
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date
    """, (start, end))
    water = cur.fetchall()

    conn.close()

    dates = [r[0] for r in rows]
    cals  = [r[1] for r in rows]

    # graph
    graph_file = None
    if dates:
        plt.figure()
        plt.plot(dates, cals, marker="o")
        plt.xticks(rotation=45, ha="right")
        plt.title("Weekly Calories Trend")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.tight_layout()

        graph_file = f"weekly_{start}_to_{end}.png".replace(":", "_")
        plt.savefig(os.path.join(REPORT_DIR, graph_file), dpi=150)
        plt.close()

    return render_template(
        "report.html",
        start_date=start,
        end_date=end,
        daily=rows,
        water=water,
        graph_file=graph_file
    ) 
@app.route("/report/pdf")
def report_pdf():
    end = request.args.get("end") or date.today().isoformat()
    start = request.args.get("start") or (date.fromisoformat(end) - timedelta(days=6)).isoformat()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT date as log_date,
               meal_name,
               calories
        FROM meals
        WHERE date BETWEEN ? AND ?
        ORDER BY date
    """, (start, end))
    meals = cur.fetchall()

    cur.execute("""
        SELECT date as log_date,
               SUM(glasses) as glasses
        FROM water
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date
    """, (start, end))
    water = cur.fetchall()

    conn.close()

    pdf_name = f"weekly_report_{start}_to_{end}.pdf".replace(":", "_")
    pdf_path = os.path.join(BASE_DIR, pdf_name)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Arogya Weekly Report")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Date range: {start} to {end}")
    y -= 24

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Meals Logged")
    y -= 16
    c.setFont("Helvetica", 10)

    if not meals:
        c.drawString(50, y, "No meals logged in this period.")
        y -= 14
    else:
        for d, meal_name, cal in meals:
            if y < 80:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, f"{d}  -  {meal_name}  ({cal} kcal)")
            y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Water Intake (per day)")
    y -= 16
    c.setFont("Helvetica", 10)

    if not water:
        c.drawString(50, y, "No water entries in this period.")
    else:
        for d, g in water:
            if y < 80:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, f"{d}  -  {g} glasses")
            y -= 14

    c.showPage()
    c.save()

    return send_file(pdf_path, as_attachment=True)


# -----------------------------------
# RUN APP
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
