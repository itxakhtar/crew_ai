# app.py
from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
import sqlite3
import time
import google.api_core.exceptions as gexc

# -------------------
# Load API Key
# -------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
genai.configure(api_key=API_KEY)

# -------------------
# Function: Get Available Model
# -------------------
def get_supported_model():
    """
    List all models and pick the first one that supports generate_content.
    """
    try:
        models = genai.list_models()
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                return m.name
        return None
    except Exception as e:
        st.error(f"Error listing models: {e}")
        return None

# -------------------
# Function: Gemini Response
# -------------------
def get_gemini_response(question, prompt, model_name):
    """
    Generates SQL query using a supported Gemini model.
    Retries if quota is exceeded.
    """
    full_prompt = f"{prompt}\nQ: {question}\nSQL:"
    
    while True:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([full_prompt])
            return response.text.strip()
        except gexc.ResourceExhausted:
            st.warning("🚨 Gemini API quota exceeded. Waiting 60 seconds before retrying...")
            time.sleep(60)
        except Exception as e:
            return f"❌ Error: {e}"

# -------------------
# Function: Execute SQL Query
# -------------------
def read_sql_query(sql, db="student.db"):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        return f"SQL Error: {e}"

# -------------------
# Streamlit UI
# -------------------
st.set_page_config(page_title="Natural Language → SQL Query", layout="wide")
st.title("🧠 Natural Language → SQL Query with Gemini")
st.markdown("Convert plain English questions into SQL queries and execute them on a SQLite database.")

# User input
question = st.text_input("Enter your question in plain English:")

# Prompt template
prompt_template = """
You are an expert AI assistant specializing in converting natural language questions into SQL queries.

The SQL database is named STUDENT and contains the following columns:
- NAME (VARCHAR)
- CLASS (VARCHAR)
- SECTION (VARCHAR)
- MARKS (INT)

Rules:
1. Only output the SQL query.
2. No explanations or comments.
3. Use proper SQL syntax.
4. Use WHERE for filtering.
5. Use COUNT(), AVG(), MAX(), etc. for aggregation.

Examples:

Q: How many student records are present?
SQL: SELECT COUNT(*) FROM STUDENT;

Q: List all students in the Data Science class.
SQL: SELECT * FROM STUDENT WHERE CLASS='Data Science';
"""

# -------------------
# Main logic
# -------------------
submit_button = st.button("Generate SQL Query & Execute")

if submit_button and question:
    with st.spinner("Fetching available model..."):
        model_name = get_supported_model()
        if not model_name:
            st.error("❌ No supported models found for generate_content.")
        else:
            st.info(f"Using model: {model_name}")

            with st.spinner("Generating SQL query..."):
                sql_query = get_gemini_response(question, prompt_template, model_name)
                st.subheader("Generated SQL Query")
                st.code(sql_query, language="sql")

            with st.spinner("Executing SQL query..."):
                results = read_sql_query(sql_query)
                st.subheader("Query Results")

                if isinstance(results, str) and results.startswith("SQL Error"):
                    st.error(results)
                elif len(results) == 0:
                    st.info("No records found.")
                else:
                    st.table(results)
