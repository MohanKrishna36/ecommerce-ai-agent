import matplotlib.pyplot as plt
import io
import base64
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