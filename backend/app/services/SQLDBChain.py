#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv, find_dotenv

import gradio as gr

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

# --- 1. Load environment variables ---
load_dotenv(find_dotenv())
DB_URL = os.getenv("DB_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# --- 2. Initialize SQL database and agent ---

db = SQLDatabase.from_uri(DB_URL)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    temperature=0,
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    handle_parsing_errors=True
)

# --- 3. Define query processing function ---

def process_query(user_question: str) -> str:
    try:
        # Run the agent
        result = agent_executor.invoke(user_question)
        
        # If result is a dict with 'output' key, extract it
        if isinstance(result, dict) and "output" in result:
            output_text = result["output"]
        else:
            # Otherwise, just stringify the whole result
            output_text = str(result)
        
        # Optionally format output — for example, add line breaks after commas
        formatted = output_text.replace(", ", ",\n")
        
        return formatted
    except Exception as e:
        return f"Error: {e}"

# --- 4. Gradio Interface Definition ---

with gr.Blocks(theme=gr.themes.Soft(), title="SQL Agent GUI") as iface:
    gr.Markdown(
        """
        # 🤖 Natural Language to SQL Agent
        Enter a question in plain English about your database.
        The AI agent will convert it to an SQL query, execute it, and return the answer.
        """
    )

    query_input = gr.Textbox(
        lines=4,
        label="Your Question",
        placeholder="e.g., How many agents are there? List their names and commission rates."
    )

    query_output = gr.Textbox(
        label="Agent Response",
        lines=8,
        interactive=False  # read-only output box
    )

    submit_button = gr.Button("Ask Agent", variant="primary")

    submit_button.click(
        fn=process_query,
        inputs=query_input,
        outputs=query_output
    )

    gr.Markdown("---")
    gr.Markdown(
        "### Example Questions:\n"
        "- *List the names of all agents.*\n"
        "- *What is the total number of orders?*\n"
        "- *Show me the agent ID, name, and commission rate for agents with a commission rate greater than 4%, and sort them by their last name in descending order.*"
    )

if __name__ == "__main__":
    iface.launch()
