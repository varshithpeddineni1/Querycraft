# ⚡ QueryCraft
### AI-Powered SQL Query Generator

Turn plain English into perfect SQL instantly!
Powered by Groq's LLaMA 3.3 70B

## 🎯 What It Does
- Converts natural language to SQL
- Supports MySQL, PostgreSQL, SQLite, 
  SQL Server and Oracle
- Explains every part of the query
- Gives optimization tips
- Shows alternative approaches
- Download query as .sql file

## 💡 Example
Input:
"Show top 5 customers by total spending"

Output:
SELECT u.name, SUM(o.total_amount) as total
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.name
ORDER BY total DESC
LIMIT 5;

## 🛠️ Tech Stack
- Python
- Groq AI (LLaMA 3.3 70B)
- Streamlit
- Python-dotenv

## 🚀 Run Locally
git clone https://github.com/varshithpeddineni1/querycraft.git
cd querycraft
pip install -r requirements.txt
streamlit run app.py

## 🚀 Live Demo
👉 https://querycrafts.streamlit.app/

## 👨‍💻 Built By
Varshith Peddineni

