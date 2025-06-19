import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from app.llm.llm import get_analytics_response

# Helper function to convert matplotlib figure to base64
def fig_to_base64(fig):
    import io
    import base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# Custom CSS for WhatsApp-like chat
st.html("""
<style>
    .chat-container {
        width: 100%;
        max-width: 660px;
        margin: 0 auto;
        font-family: "Segoe UI", Helvetica, sans-serif;
    }
    
    .user-message {
        background-color: #DCF8C6;
        color: #000;
        border-radius: 7.5px 0 7.5px 7.5px;
        padding: 8px 12px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }
    
    .assistant-message {
        background-color: #FFFFFF;
        color: #000;
        border-radius: 0 7.5px 7.5px 7.5px;
        padding: 8px 12px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }
    
    .chat-window {
        height: 400px;
        overflow-y: auto;
        padding: 5px;
        background-color: #ECE5DD;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .message-container {
        overflow: hidden;
        width: 100%;
    }
    
    .timestamp {
        font-size: 0.7em;
        color: #888;
        margin-top: 3px;
        text-align: right;
    }
    
    .assistant-table {
        background-color: white;
        border-radius: 8px;
        padding: 8px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }
    
    .assistant-image {
        max-width: 70%;
        border-radius: 8px;
        margin: 5px 0;
        float: left;
        clear: both;
        box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13);
    }
</style>
""")

# App header
st.html("<h1 style='font-size: 1.5em; text-align: center;'>📈 Analytics Assistant</h1>")
st.html("<h3 style='font-size: 0.9em; text-align: center; color: #666; margin-bottom: 20px;'>I can show tables, charts, and analyze data!</h3>")

USER = "user"
ASSISTANT = "assistant"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate chat HTML
def render_chat():
    chat_html = """
    <div class="chat-container">
        <div class="chat-window" id="chat-window">
    """
    
    for msg in st.session_state.messages:
        if msg["role"] == USER:
            chat_html += f"""
            <div class="message-container">
                <div class="user-message">
                    {msg["content"]}
                    <div class="timestamp">Just now</div>
                </div>
            </div>
            """
        else:
            if msg["type"] == "text":
                chat_html += f"""
                <div class="message-container">
                    <div class="assistant-message">
                        {msg["content"]}
                        <div class="timestamp">Just now</div>
                    </div>
                </div>
                """
            elif msg["type"] == "table":
                # Convert dataframe to HTML table
                table_html = msg["content"].to_html(index=False, border=0, classes="dataframe")
                chat_html += f"""
                <div class="message-container">
                    <div class="assistant-table">
                        {table_html}
                        <div class="timestamp">Just now</div>
                    </div>
                </div>
                """
            elif msg["type"] == "image":
                chat_html += f"""
                <div class="message-container">
                    <div class="assistant-image">
                        <img src="{msg['content']}" style="width:100%; border-radius:8px;">
                        <div class="timestamp">Just now</div>
                    </div>
                </div>
                """
    
    chat_html += """
        </div>
    </div>
    <script>
        var chatWindow = document.getElementById('chat-window');
        if(chatWindow) { chatWindow.scrollTop = chatWindow.scrollHeight; }
    </script>
    """
    return chat_html

# Render the chat
st.html(render_chat())

# Chat input
prompt = st.chat_input("Ask for data, charts, or analysis...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": USER, "content": prompt})
    
    data, summary = get_analytics_response(prompt)
    
    if data is None:
        st.session_state.messages.append({
            "role": ASSISTANT, 
            "type": "text",
            "content": "Can not retrieve data. Refine you prompt and try again."
        })
    else:
        # Convert the dataframe to an image (matplotlib table)
        fig, ax = plt.subplots()
        ax.axis('off')
        tbl = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1, 1.5)
        img_base64 = "data:image/png;base64," + fig_to_base64(fig)
        plt.close(fig)
        st.session_state.messages.append({
            "role": ASSISTANT,
            "type": "image",
            "content": img_base64
        })
        
        st.session_state.messages.append({
            "role": ASSISTANT, 
            "type": "text",
            "content": summary
        })
    
    # # Generate appropriate assistant response
    # if "table" in prompt.lower():
    #     # Create sample dataframe
    #     data = pd.DataFrame({
    #         'Product': ['Apples', 'Oranges', 'Bananas'],
    #         'Sales': [100, 200, 150],
    #         'Profit': [20, 40, 30]
    #     })
    #     st.session_state.messages.append({
    #         "role": ASSISTANT, 
    #         "type": "table",
    #         "content": data
    #     })
    # elif "image" in prompt.lower():
    #     # Use a sample image
    #     image_url = "https://via.placeholder.com/300x200.png?text=Sample+Image"
    #     st.session_state.messages.append({
    #         "role": ASSISTANT, 
    #         "type": "image",
    #         "content": image_url
    #     })
    # elif "chart" in prompt.lower():
    #     # Generate and save a sample plot
    #     fig, ax = plt.subplots()
    #     ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    #     ax.set_title('Sample Chart')
    #     st.session_state.messages.append({
    #         "role": ASSISTANT, 
    #         "type": "image",
    #         "content": "data:image/png;base64," + fig_to_base64(fig)
    #     })
    # else:
    #     # Default text response
    #     st.session_state.messages.append({
    #         "role": ASSISTANT, 
    #         "type": "text",
    #         "content": f"I received: '{prompt}'. Here's what I can show:\n\n• Say 'table' for sample data\n• Say 'image' for a picture\n• Say 'chart' for a graph"
    #     })
    
    st.rerun()
