import os
import requests
import sqlite3
import base64
import io
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load API key from .env file
load_dotenv()

app = Flask(__name__)
conn = sqlite3.connect("ecommerce.db", check_same_thread=False)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"
URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Prompt builder
def build_prompt(question):
    return f"""
You are a helpful assistant that converts user questions into SQL queries.

Use only the following tables and columns:

1. total_sales(date, item_id, total_sales, total_units_ordered)
2. ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
3. eligibility(product_id, is_eligible)

User question: {question}

Only respond with SQL. No markdown or explanation.
"""


# LLM call
def question_to_sql(question):
    prompt = build_prompt(question)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content'].strip("```sql").strip("```").strip()
        except Exception:
            print("⚠️ Unexpected response:", response.json())
            return None
    else:
        print("❌ LLM ERROR:", response.status_code, response.text)
        return None

# Optional: generate visualization as base64

def generate_chart(columns, results):
    try:
        if len(columns) == 2 and len(results) > 0:
            x = [str(row[columns[0]]) for row in results]
            y = [row[columns[1]] for row in results]
            plt.figure(figsize=(8, 4))
            plt.bar(x, y, color='skyblue')
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])
            plt.title(f"{columns[1]} by {columns[0]}")
            plt.xticks(rotation=45)
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format="png")
            buf.seek(0)
            chart_base64 = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()
            plt.close()
            return chart_base64
    except Exception as e:
        print("⚠️ Chart generation failed:", str(e))
    return None

# API routes
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' in request"}), 400

    sql_query = question_to_sql(question)

    if not sql_query:
        return jsonify({"error": "Failed to generate SQL"}), 500

    try:
        cursor = conn.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        chart = generate_chart(columns, results)
        return jsonify({"query": sql_query, "results": results, "chart": chart})
    except Exception as e:
        return jsonify({"error": str(e), "query": sql_query}), 500

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
