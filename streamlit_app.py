import streamlit as st
import anthropic
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Claude AI Assistant", layout="wide")

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

def initialize_client():
    """Initialize the Anthropic client with the API key."""
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing client: {str(e)}")
        return None

# Sidebar for API key configuration
with st.sidebar:
    st.title("Configuration")
    api_key = st.text_input("Enter your Anthropic API key:", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.session_state.api_key_configured = True
    
    st.markdown("---")
    st.markdown("### Chat History")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
st.title("Claude AI Assistant")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Claude:** {message['content']}")

# Chat input
user_input = st.text_area("Type your message here:", key="user_input")
if st.button("Send") and user_input:
    if not st.session_state.api_key_configured:
        st.error("Please configure your API key in the sidebar first.")
    else:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        try:
            # Initialize client and send message
            client = initialize_client()
            if client:
                message = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # Add Claude's response to chat history
                response_content = message.content[0].text
                st.session_state.chat_history.append({"role": "assistant", "content": response_content})
                
                # Rerun to update the display
                st.rerun()
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Created with Streamlit and Claude API")
