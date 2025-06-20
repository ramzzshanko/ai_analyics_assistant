from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
import os
from app import logger

from app.tools.tools import generate_html_table, plot_area, plot_bar, plot_heatmap, plot_line, plot_pie, run_sql_query


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")

with open("config/duckdb_sql_llm.mod", "r") as file:
    SQL_SYSTEM_PROMPT = file.read()

with open("config/suggest_viz.mod", "r") as file:
    SUGGEST_VIZ_PROMPT = file.read()
    
with open("config/summarize_data.mod", "r") as file:
    SUMMARIZE_DATA = file.read()

def get_groq_client():
    client = ChatGroq(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        temperature=0.1
    )
    return client

def get_visualization(prompt: str):
    client = get_groq_client().bind_tools([plot_bar, plot_heatmap, plot_pie, plot_line, plot_area, generate_html_table])
    
    # Define system message
    system_message = SystemMessage(
        content=SUGGEST_VIZ_PROMPT
    )
        
    # Define user message
    user_message = HumanMessage(
        content=prompt
    )
    
    # Get response from Groq model
    response = client.invoke([system_message, user_message])
    
    return response.content


def summarize_data(prompt: str):
    client = get_groq_client()
    # Define system message
    system_message = SystemMessage(
        content=SUMMARIZE_DATA
    )
        
    # Define user message
    user_message = HumanMessage(
        content=prompt
    )
    
    # Get response from Groq model
    response = client.invoke([system_message, user_message])
    
    return response.content


def get_analytics_response(prompt: str, chat_history=None):
    client = get_groq_client()
    
    # Prepare chat history if provided
    messages = []
    if chat_history:
        messages.extend(chat_history)
    # Add system and user messages for current turn
    messages.append(SystemMessage(content=SQL_SYSTEM_PROMPT))
    messages.append(HumanMessage(content=prompt))
    
    # Get response from Groq model
    sql_response = client.invoke(messages)
    
    logger.info(sql_response.content)
    
    if sql_response.content == "Invalid query":
        print("Invalid Query")
        return None, None, messages
    
    df_response = run_sql_query(sql_response.content)  
    
    suggested_viz = summarize_data(prompt + " # " + df_response.to_string())
    
    # Update chat history with latest messages and response
    messages.append(sql_response)
    
    return df_response, suggested_viz, messages