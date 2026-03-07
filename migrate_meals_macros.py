import sqlite3, os

# ✅ Use the SAME DB location as your Flask app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPDATA_DIR = os.path.join(os.environ.get("APPDATA", BASE_DIR), "Arogya")
DB_PATH = os.path.join(APPDATA_DIR, "database.db")

print("Migrating DB:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def add_col(table, col_def):
    try:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
        print(f"Added {table}.{col_def}")
    except Exception as e:
        print(f"ℹ Skipped {table}.{col_def} ({e})")

# Add missing columns to meals
add_col("meals", "meal_type TEXT")
add_col("meals", "food_item_id INTEGER")
add_col("meals", "quantity REAL DEFAULT 1")
add_col("meals", "protein REAL DEFAULT 0")
add_col("meals", "carbs REAL DEFAULT 0")
add_col("meals", "fat REAL DEFAULT 0")
add_col("meals", "sugar REAL DEFAULT 0")

conn.commit()
conn.close()
print(" Done")