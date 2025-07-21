import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.execute("PRAGMA table_info(ad_sales)")
print("📋 Columns in 'ad_sales':")
for col in cursor.fetchall():
    print("-", col[1])
