import sqlite3

conn = sqlite3.connect("ecommerce.db")

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("📦 Tables in DB:", tables)

print("\n📋 Columns in 'total_sales':")
for row in conn.execute("PRAGMA table_info(total_sales);").fetchall():
    print(f"- {row[1]} ({row[2]})")
