from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

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

@app.route("/meal-plan")
def meal_plan():
    plan_name = request.args.get("name")

    plans = {
        "High-Protein Gain Plan": [
            "Breakfast: Eggs + Oats + Milk",
            "Lunch: Chicken + Rice + Vegetables",
            "Dinner: Fish + Sweet Potatoes"
        ],

        "Balanced Diet Plan": [
            "Breakfast: Oats + Berries",
            "Lunch: Grilled Chicken + Rice",
            "Dinner: Mixed Vegetables + Fish"
        ],

        "Weight Loss Plan": [
            "Breakfast: Scrambled Eggs",
            "Lunch: Chicken Salad",
            "Dinner: Vegetable Soup"
        ],

        "Low-Carb Plan": [
            "Breakfast: Greek Yogurt",
            "Lunch: Chicken + Broccoli",
            "Dinner: Salmon + Spinach"
        ]
    }

    selected = plans.get(plan_name, None)
    return render_template("mealplan.html", name=plan_name, items=selected)

# -----------------------------------
# BMI CALCULATOR
# -----------------------------------

@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    result = None
    category = None
    suggested_plans = []

    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"]) / 100  # convert cm to meters

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

        result = bmi_value

    return render_template("bmi.html",
                           bmi=result,
                           category=category,
                           suggested_plans=suggested_plans)

# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
 