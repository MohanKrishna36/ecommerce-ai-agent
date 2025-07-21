import sqlite3
import requests

# Connect to DB
conn = sqlite3.connect("ecommerce.db")

# OpenRouter API setup
API_KEY = "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"
MODEL = "openai/gpt-3.5-turbo"
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def ask_question(question):
    prompt = f"""
You are a helpful assistant who converts user questions into SQL queries.

Use only the following tables and columns:

1. total_sales(date, item_id, total_sales, total_units_ordered)
2. ad_sales(product_id, impressions, clicks, cpc, roas)
3. eligibility(product_id, is_eligible)

User question: {question}

Only respond with a SQL query compatible with SQLite. Do not add comments or explanations.
"""


    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        sql = response.json()["choices"][0]["message"]["content"]
        sql = sql.strip("```sql").strip("```").strip()
        print("🔹 Generated SQL:\n", sql)

        try:
            cursor = conn.execute(sql)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            print("\n✅ Query Result:")
            for row in rows:
                print(dict(zip(columns, row)))
        except Exception as e:
            print("❌ SQL Execution Error:", e)
    else:
        print("❌ LLM Error:", response.status_code)
        print(response.text)

# Example usage
ask_question("What is my total sales?")
