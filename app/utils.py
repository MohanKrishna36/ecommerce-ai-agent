import matplotlib.pyplot as plt
import io
import base64
import tiktoken

def generate_chart(columns, results):
    # try:
    #     if len(columns) == 2 and len(results) > 0:
    #         x = [str(row[columns[0]]) for row in results]
    #         y = [row[columns[1]] for row in results]
    #         plt.figure(figsize=(8, 4))
    #         plt.bar(x, y, color='skyblue')
    #         plt.xlabel(columns[0])
    #         plt.ylabel(columns[1])
    #         plt.title(f"{columns[1]} by {columns[0]}")
    #         plt.xticks(rotation=45)
    #         buf = io.BytesIO()
    #         plt.tight_layout()
    #         plt.savefig(buf, format="png")
    #         buf.seek(0)
    #         chart_base64 = base64.b64encode(buf.read()).decode("utf-8")
    #         buf.close()
    #         plt.close()
    #         return chart_base64
    # except Exception as e:
    #     print("⚠ Chart generation failed:", str(e))
    return None

def generate_summary(question, columns, results):
    try:
        if not results:
            return "No data found for your question."

        if len(results) == 1 and len(columns) == 1:
            key = columns[0]
            value = results[0][key]
            return f"The result for your question is: {value}"
        
        elif len(results) == 1:
            parts = [f"{col}: {results[0][col]}" for col in columns]
            return "Here are the details: " + ", ".join(parts)

        else:
            return f"Got {len(results)} rows. Showing top result: " + ", ".join(
                [f"{col}: {results[0][col]}" for col in columns]
            )

    except Exception as e:
        print("⚠ Summary generation failed:", str(e))
        return "Result fetched successfully."


def trim_to_16000_tokens(text: str) -> str:
    enc = tiktoken.encoding_for_model("gpt-4")  # or "gpt-3.5-turbo", etc.
    tokens = enc.encode(text)
    trimmed_tokens = tokens[:10000]  # Slice to 16,000 tokens
    return enc.decode(trimmed_tokens)


def build_natural_language_prompt(user_question, sql_query, sql_output):
    sql_trimmed = trim_to_16000_tokens(str(sql_output))
    prompt = f"""
You are a helpful assistant. Your job is to answer the user's question using the data provided.

User Question: "{user_question}"

Query:
{sql_query}

Data:
{sql_trimmed}

Instructions:
- Do not mention table names, column names, SQL, or any internal terms.
- Do not explain how things are calculated.
- Do not say “the result is from a query” or “SQL output shows…” etc.
- Directly answer the question as if you're talking to a normal person, not a developer.
- Be concise and natural.
- Do not skip or summarize with "..." or phrases like "and so on".
- Include every item and value shown in the data.
- If there's no data, just say: "No data found for your question."
Don't skip or summarize any items. List every single item with its CTR (click-through rate) calculated as clicks divided by impressions. Give the result in full, even if it is long. Do not say "and so on."

Now, write the answer in plain and complete English, listing all values clearly without skipping anything.
"""
    return prompt

def generate_chart_prompt(user_prompt, sql_query, sql_response):
    sql_trimmed = trim_to_16000_tokens(str(sql_response))
    prompt = f"""
You are a data visualization assistant.
Based on the following:
- *User Prompt*: {user_prompt}
- *SQL Query Used*: {sql_query}
- *SQL Output (as JSON)*: {sql_response}

Generate a Python code snippet using matplotlib or plotly to visualize the result. 
The code should ONLY return the plot (no print statements or explanations), and assume all required libraries are imported.
    """
    return prompt.strip()

def exec_python_code(code: str):
    """
    Executes Python code that generates a matplotlib chart and returns it as base64 image.
    """
    # Create a local dictionary to isolate exec environment
    local_env = {}
    try:
        exec(code, {"plt": plt}, local_env)
        
        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Encode image to base64
        encoded_image = base64.b64encode(buf.read()).decode("utf-8")
        return encoded_image
    except Exception as e:
        return f"Error executing code: {str(e)}"