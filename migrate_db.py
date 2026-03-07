import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPDATA_DIR = os.path.join(os.environ.get("APPDATA", BASE_DIR), "Arogya")
DB_PATH = os.path.join(APPDATA_DIR, "database.db")

print("MIGRATION DB PATH:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def add_col(table, col_def):
    try:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
        print(f"✅ Added {table}.{col_def}")
    except Exception as e:
        print(f"ℹ Skipped {table}.{col_def.split()[0]} ({e})")

# Add user_id and created_at to meals + water
add_col("meals", "user_id INTEGER")
add_col("meals", "created_at TEXT DEFAULT CURRENT_TIMESTAMP")

add_col("water", "user_id INTEGER")
add_col("water", "created_at TEXT DEFAULT CURRENT_TIMESTAMP")

conn.commit()
conn.close()
print("✅ Done")