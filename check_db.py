import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
print("CHECKING DB PATH:", DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cur.fetchall())

cur.execute("SELECT * FROM meals")
print("Meals:", cur.fetchall())

cur.execute("SELECT * FROM water")
print("Water:", cur.fetchall())

conn.close()