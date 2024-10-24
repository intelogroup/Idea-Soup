import streamlit as st
from anthropic import Anthropic
import os
import sys
import subprocess
from datetime import datetime

def install_requirements():
    """Install required packages if they're not already installed"""
    try:
        import streamlit
        import anthropic
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "anthropic"])
            st.success("Successfully installed required packages!")
            st.rerun()
        except subprocess.CalledProcessError:
            st.error("Failed to install required packages. Please install streamlit and anthropic manually.")

# Install requirements if needed
install_requirements()

# Page configuration
st.set_page_config(
    page_title="Claude AI Assistant",
    layout="wide"
)

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

def initialize_client():
    """Initialize the Anthropic client with the API key."""
    try:
        client = Anthropic(api_key=st.session_state.api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing client: {str(e)}")
        return None

# Add version info to sidebar
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
    
    st.markdown("---")
    st.markdown("### App Info")
    st.markdown(f"Python version: {sys.version.split()[0]}")
    try:
        import streamlit
        st.markdown(f"Streamlit version: {streamlit.__version__}")
    except:
        st.markdown("Streamlit version: Not found")
    try:
        import anthropic
        st.markdown(f"Anthropic version: {anthropic.__version__}")
    except:
        st.markdown("Anthropic version: Not found")

# Main chat interface
st.title("Claude AI Assistant")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Claude:** {message['content']}")

# Chat input
user_input = st.text_area("Type your message here:", key="user_input", height=100)
send_button = st.button("Send", type="primary")

if send_button and user_input:
    if not st.session_state.api_key_configured:
        st.error("Please configure your Anthropic API key in the sidebar first.")
    else:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        try:
            # Initialize client and send message
            with st.spinner("Claude is thinking..."):
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
st.markdown("""
    <div style='text-align: center'>
        Created with Streamlit and Claude API<br>
        Last updated: April 2024
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # This will only run if the script is run directly
    pass
