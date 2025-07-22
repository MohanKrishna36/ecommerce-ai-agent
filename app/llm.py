import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def build_prompt(question):
    return f"""
You are an expert in SQLite. Given the following natural language query, generate a valid SQLite SQL query:

User Query: "What is my total sales every month?"

Only return the SQL query. Do not use MySQL or PostgreSQL syntax. Use only SQLite-supported functions and syntax.


Use only the following tables and columns:

1. total_sales(date, item_id, total_sales, total_units_ordered)
the below is the example data for the table:
date,item_id,total_sales,total_units_ordered
2025-06-01,0,309.99,1

2. ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
date,item_id,ad_sales,impressions,ad_spend,clicks,units_sold
2025-06-01,0,332.96,1963,16.87,8,3

3. eligibility(eligibility_datetime_utc, item_id, eligibility, message)
2025-06-04 8:50:07,29,0,This product's cost to Amazon does not allow us to meet customers’ pricing expectations. Consider reducing the cost. It may take a few weeks for your product to become eligible to advertise after you reduce the cost.
2025-06-04 8:50:07,270,1,
2025-06-04 8:50:07,31,1,
2025-06-04 8:50:07,26,1,

these are the only tables and columns you can use. if user asks something you must use the columns which are available in the tables above.
strictly use the columns in the tables above. do not use any other columns or tables.
Only use the available functions in the sql, dont use functions which are not available in the sql.
User question: {question}
Strictly Dont use you own column names or table names. use only the columns and tables which are available in the above tables.
Only respond with SQL. No markdown or explanation.
"""

def question_to_sql(question):
    prompt = build_prompt(question)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        try:
            # 🟢 Print entire raw response
            print("🧠 Raw LLM response JSON:")
            print(response.json())

            # Extract and clean the SQL
            raw_sql = response.json()['choices'][0]['message']['content']
            print("\n📄 Raw SQL string from model:")
            print(raw_sql)

            cleaned_sql = (
                raw_sql.replace("sql", "")
                       .replace("", "")
                       .strip()
            )

            print("\n✅ Cleaned SQL to be executed:")
            print(cleaned_sql)

            return cleaned_sql
        except Exception as e:
            print("⚠ Unexpected response or error:", str(e))
            return None
    else:
        print("❌ LLM ERROR:", response.status_code)
        print(response.text)
        return None
