from flask import Blueprint, request, jsonify, render_template
from .llm import question_to_sql, call_llm
from .db import get_db_connection
from .utils import generate_chart, generate_summary, build_natural_language_prompt, generate_chart_prompt, exec_python_code

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@main.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    print("Received data:", data)  # Debugging line
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' in request"}), 400

    sql_query = question_to_sql(question)
    if not sql_query:
        return jsonify({"error": "Failed to generate SQL"}), 500

    try:
        conn = get_db_connection()
        cursor = conn.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        conn.close()

        # Generate chart (optional)
        chart = generate_chart(columns, results)

        # Generate human-readable summary
        prompt = build_natural_language_prompt(question, sql_query, results)
        chart_prompt = generate_chart_prompt(question, sql_query, results)
        english_response = call_llm(prompt, 
                                    system="You are a helpful assistant that explains SQL query results in simple English, without using terms like sql or anything.",
                                    model="openai/gpt-3.5-turbo")
        chart_code = call_llm(chart_prompt, 
                                  system="You are a helpful assistant that generates charts based on SQL query results.",
                                  model="openai/gpt-3.5-turbo")
        
        image = exec_python_code(chart_code)
        return jsonify({
            "query": sql_query,
            "results": results,
            "chart": image,
            "summary": english_response or "No summary generated"
        })

    except Exception as e:
        return jsonify({"error": str(e), "query": sql_query}), 500