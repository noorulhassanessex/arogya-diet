import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPDATA_DIR = os.path.join(os.environ.get("APPDATA", BASE_DIR), "Arogya")
DB_PATH = os.path.join(APPDATA_DIR, "database.db")

print("FOODS MIGRATION DB PATH:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# foods table
cur.execute("""
CREATE TABLE IF NOT EXISTS foods (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE,
  calories REAL DEFAULT 0,
  protein REAL DEFAULT 0,
  carbs REAL DEFAULT 0,
  fat REAL DEFAULT 0,
  sugar REAL DEFAULT 0
)
""")

def add_col(table, col_def):
    try:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
        print(f"✅ Added {table}.{col_def}")
    except Exception as e:
        print(f"ℹ Skipped {table}.{col_def.split()[0]} ({e})")

# add columns to meals so tracker can store macros + selection
add_col("meals", "meal_type TEXT")
add_col("meals", "food_item_id INTEGER")
add_col("meals", "quantity REAL DEFAULT 1")
add_col("meals", "protein REAL DEFAULT 0")
add_col("meals", "carbs REAL DEFAULT 0")
add_col("meals", "fat REAL DEFAULT 0")
add_col("meals", "sugar REAL DEFAULT 0")

# seed foods if empty
cur.execute("SELECT COUNT(*) FROM foods")
if cur.fetchone()[0] == 0:
    seed = [
        ("Oats", 150, 5, 27, 3, 1),
        ("Boiled Eggs", 140, 12, 1, 10, 0),
        ("Chicken Breast", 165, 31, 0, 3.6, 0),
        ("Rice (cooked)", 130, 2.7, 28, 0.3, 0),
        ("Banana", 105, 1.3, 27, 0.3, 14),
    ]
    cur.executemany("""
        INSERT INTO foods (name, calories, protein, carbs, fat, sugar)
        VALUES (?, ?, ?, ?, ?, ?)
    """, seed)
    print("✅ Seeded foods")

conn.commit()
conn.close()
print("✅ Done")