from flask import Blueprint, request, jsonify, render_template
from .llm import question_to_sql
from .db import get_db_connection
from .utils import generate_chart

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@main.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
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


        return jsonify({
            "query": sql_query,
            "results": results,
            "chart": chart,
          
        })

    except Exception as e:
        return jsonify({"error": str(e), "query": sql_query}), 500