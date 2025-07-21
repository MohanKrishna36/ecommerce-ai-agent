from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

# DB setup
conn = sqlite3.connect("ecommerce.db", check_same_thread=False)

# OpenRouter setup
API_KEY = "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"
MODEL = "openai/gpt-3.5-turbo"  # ✅ Add this line
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}


# Prompt builder
def build_prompt(question):
    return f"""
You are a helpful assistant that converts user questions into SQL queries.

Use only the following tables and columns:

1. total_sales(date, item_id, total_sales, total_units_ordered)
2. ad_sales(product_id, impressions, clicks, cpc, roas)
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
        return response.json()['choices'][0]['message']['content'].strip("```sql").strip("```").strip()
    else:
        print("❌ LLM ERROR:", response.status_code)
        print(response.text)
        return None


# API route
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
        return jsonify({"query": sql_query, "results": results})
    except Exception as e:
        return jsonify({"error": str(e), "query": sql_query}), 500
    
@app.route("/", methods=["GET"])
def home():
    return "✅ API is running. Use POST /ask with a question."


if __name__ == "__main__":
    app.run(debug=True)
