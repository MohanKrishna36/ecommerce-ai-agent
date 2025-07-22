import pandas as pd
import sqlite3
import os

def get_db_connection():
    return sqlite3.connect("ecommerce.db")


# Create the SQLite DB file
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Load CSVs from the 'data' folder
data_dir = "data"

# Load Eligibility Table
eligibility_df = pd.read_csv(os.path.join(data_dir, "eligibility.csv"))
eligibility_df.to_sql("eligibility", conn, if_exists="replace", index=False)

# Load Ad Sales Table
ad_sales_df = pd.read_csv(os.path.join(data_dir, "ad_sales.csv"))
ad_sales_df.to_sql("ad_sales", conn, if_exists="replace", index=False)

# Load Total Sales Table
total_sales_df = pd.read_csv(os.path.join(data_dir, "total_sales.csv"))
total_sales_df.to_sql("total_sales", conn, if_exists="replace", index=False)

print("✅ All tables loaded into ecommerce.db successfully.")

# Close connection
conn.close()