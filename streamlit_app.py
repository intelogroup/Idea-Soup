import streamlit as st
import anthropic
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Claude AI Assistant", layout="widimport streamlit as st
from anthropic import Anthropic
import os
from datetime import datetime
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Page configuration
st.set_page_config(page_title="Claude AI Assistant", layout="wide")

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

def get_youtube_id(url):
    """Extract YouTube video ID from URL"""
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_transcript(url):
    """Get transcript of YouTube video"""
    try:
        video_id = get_youtube_id(url)
        if not video_id:
            return "Invalid YouTube URL"
        
        # Get video information
        yt = YouTube(url)
        video_title = yt.title
        
        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format transcript
        formatted_transcript = f"Title: {video_title}\n\nTranscript:\n"
        for entry in transcript:
            timestamp = int(entry['start'])
            minutes = timestamp // 60
            seconds = timestamp % 60
            formatted_transcript += f"[{minutes}:{seconds:02d}] {entry['text']}\n"
        
        return formatted_transcript
        
    except Exception as e:
        return f"Error getting transcript: {str(e)}"

def initialize_client():
    """Initialize the Anthropic client with the API key."""
    try:
        client = Anthropic(api_key=st.session_state.api_key)
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

# YouTube URL input
st.markdown("### YouTube Transcript")
youtube_url = st.text_input("Enter YouTube URL:")
if youtube_url:
    with st.spinner("Fetching transcript..."):
        transcript = get_video_transcript(youtube_url)
        st.text_area("Video Transcript", transcript, height=300)

# Display chat history
st.markdown("### Chat History")
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
st.markdown("Created with Streamlit and Claude API")e")

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
