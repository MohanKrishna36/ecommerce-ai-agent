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
You are an expert in SQLite. Given the following natural language query, generate a valid SQLite SQL query.

User Query: "{question}"

Only return the SQL query. Do not use MySQL or PostgreSQL syntax. Use only SQLite-supported functions and syntax.

You are restricted to use only the following tables and columns:

---

1. total_sales(date, item_id, total_sales, total_units_ordered)  
Example:
date,item_id,total_sales,total_units_ordered  
2025-06-01,0,309.99,1  
→ Note: `date` is in TEXT format. Convert it into DATE format using DATE(date) or strftime('%Y-%m-%d', date)

---

2. ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)  
Example:
2025-06-01,0,332.96,1963,16.87,8,3  
→ Note: `date` is in TEXT format. Convert it into DATE format using DATE(date) or strftime('%Y-%m-%d', date)

To calculate **RoAS (Return on Ad Spend)**:
- Use the formula: **RoAS = ad_sales / ad_spend**
- Aggregate (SUM) `ad_sales` and `ad_spend` per group (e.g., by date or item) before dividing.
- Example: `ROUND(SUM(ad_sales) / SUM(ad_spend), 2) AS roas`

---

3. eligibility(eligibility_datetime_utc, item_id, eligibility, message)  
Example:
2025-06-04 8:50:07,29,0,"This product's cost to Amazon does not allow us to meet customers’ pricing expectations."

---

Rules:
- You MUST use only the listed tables and columns.
- DO NOT invent or assume columns or tables not listed.
- DO NOT use unsupported functions — only SQLite-compatible functions are allowed.
- Convert all `date` text columns into proper DATE format using `DATE()` or `strftime()` when performing date-based grouping or filtering.
- For RoAS-related queries, follow the formula provided above.
- Your output should be a valid, executable SQLite SQL query only.
- DO NOT include any explanation, comments, or markdown formatting — only raw SQL.

Return only the SQL query.
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

# API_KEY = os.getenv("OPENROUTER_API_KEY")
def call_llm(prompt, system, model="openai/gpt-3.5-turbo"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error from LLM API: {response.status_code} - {response.text}"