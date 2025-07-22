
# 🛒 Ecommerce AI Agent 🤖

This is an AI-powered natural language interface for querying ecommerce data using SQLite. Users can ask business-related questions (e.g., "What is my total sales every month?"), and the system automatically:

✅ Converts the question into a valid SQL query
✅ Executes the SQL query on a local database
✅ Returns results, generates visualizations (bar charts), and explains the outcome in natural language

---

## 📁 Project Structure

```
ecommerce-ai-agent/
│
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # Route handlers for UI and AI interaction
│   ├── llm.py              # Handles calls to the OpenRouter API (GPT model)
│   ├── db.py               # SQLite DB connection and CSV data loading
│   ├── utils.py            # Chart generation, prompt building, and summary logic
│   └── templates/
│       └── index.html      # Frontend (HTML + JS + Plotly)
│
├── data/
│   ├── eligibility.csv     # Product eligibility info
│   ├── ad_sales.csv        # Advertisement data
│   └── total_sales.csv     # Product sales info
│
├── ecommerce.db            # Generated SQLite database
├── .env                    # Contains API key for OpenRouter
├── requirements.txt        # Python dependencies
└── README.md               # You're here!
```

---

## 🚀 Features

* 🧠 LLM (GPT-3.5) converts natural language → SQL
* 📊 Auto-generated Plotly charts
* 💬 English summary of SQL result
* 🧪 Developer mode (shows raw SQL + results)
* 📦 SQLite-based backend with three core tables

---

## 🏁 Quickstart

### 1. Clone and Navigate

```bash
git clone https://github.com/mohankrishna36/ecommerce-ai-agent.git
cd ecommerce-ai-agent
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: You need Python 3.8 or above.

### 3. Setup `.env` file

Create a `.env` file in the root directory:

```
OPENROUTER_API_KEY=your_openrouter_api_key
```

> Get your API key from: [https://openrouter.ai](https://openrouter.ai)

### 4. Prepare the Database

Ensure the `data/` folder contains:

* `eligibility.csv`
* `ad_sales.csv`
* `total_sales.csv`

Then run:

```bash
python app/db.py
```

✅ This will generate `ecommerce.db` and load all the CSV data into tables.

---

### 5. Start the Flask Server

```bash
export FLASK_APP=app
flask run
```

Go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 💡 Example Usage

Ask:

```
What is my total sales every month?
```

The AI will:

* Generate a valid SQL query on the `total_sales` table
* Return results
* Display a Plotly bar chart
* Summarize: "In January, sales were \$XYZ, in February \$ABC..." etc.

Enable **Developer Mode** to see raw SQL and result JSON.

---

## 🧱 Core Tables (SQLite)

### 1. `total_sales`

| Column                | Description        |
| --------------------- | ------------------ |
| `date`                | Text (YYYY-MM-DD)  |
| `item_id`             | Product identifier |
| `total_sales`         | Float              |
| `total_units_ordered` | Integer            |

### 2. `ad_sales`

| Column        | Description |
| ------------- | ----------- |
| `date`        | Text        |
| `item_id`     | Integer     |
| `ad_sales`    | Float       |
| `clicks`      | Integer     |
| `impressions` | Integer     |
| `ad_spend`    | Float       |
| `units_sold`  | Integer     |

### 3. `eligibility`

| Column                     | Description             |
| -------------------------- | ----------------------- |
| `eligibility_datetime_utc` | Timestamp               |
| `item_id`                  | Product ID              |
| `eligibility`              | Binary (0/1)            |
| `message`                  | Optional reason message |

---

## 🔐 Security Notes

* Your `.env` file (with API key) should **never** be committed to GitHub.
* Use `python-dotenv` to load environment variables securely.

---

## 📦 Requirements

```txt
Flask
requests
python-dotenv
pandas
matplotlib
tiktoken
plotly
```

> Install via `pip install -r requirements.txt`

---

## 📸 Screenshot

![Screenshot](https://user-images.githubusercontent.com/your-screenshot-link.jpg)

---

## 🤝 Contribution

PRs and suggestions welcome!
If you find a bug or want a new feature, open an issue.