"""
⚓ CAPTAIN AI - Streamlit Web Interface
Beautiful web app for CAPTAIN AI with real-time search and citations.
"""

import streamlit as st
import os
from captain import PerplexityClone

# Page configuration
st.set_page_config(
    page_title="⚓ CAPTAIN AI",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .captain-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .source-badge {
        background-color: #e7f3ff;
        border-left: 4px solid #1f77b4;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "ai" not in st.session_state:
    st.session_state.ai = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False


def initialize_ai(api_key):
    """Initialize the AI with the given API key"""
    try:
        st.session_state.ai = PerplexityClone(api_key=api_key)
        st.session_state.api_key_set = True
        return True
    except ValueError as e:
        st.error(f"❌ {e}")
        return False


# Sidebar
with st.sidebar:
    st.markdown("## ⚓ CAPTAIN AI Settings")
    
    # API Key input
    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        placeholder="sk-your-key-here",
        help="Get a free key at: https://platform.openai.com/signup"
    )
    
    if api_key and not st.session_state.api_key_set:
        if st.button("✅ Connect API", use_container_width=True):
            if initialize_ai(api_key):
                st.success("✅ Connected successfully!")
            st.rerun()
    
    st.divider()
    
    # Instructions
    st.markdown("""
    ### 📖 How to Use
    
    1. **Get API Key** - Free tier at [OpenAI](https://platform.openai.com/signup)
    2. **Enter API Key** - Paste it in the field above
    3. **Ask Questions** - Type any question in the chat
    4. **Get Answers** - CAPTAIN AI searches the web and provides cited answers
    
    ### ✨ Features
    - 🔍 Real-time web search
    - 📚 Cited sources for every fact
    - 💬 Multi-turn conversations
    - ⚡ Fast and accurate
    
    ### 🚀 Commands
    - `/reset` - Clear conversation history
    - `/sources` - Show all sources used
    """)
    
    st.divider()
    
    # Reset button
    if st.session_state.api_key_set and st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.ai:
            st.session_state.ai.reset_conversation()
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    ---
    **Made with ⚓ by Captain AI**
    
    Powered by OpenAI & DuckDuckGo
    
    [GitHub](https://github.com/captaintharun0507/captain-ai) | 
    [Docs](https://github.com/captaintharun0507/captain-ai#readme)
    """)


# Main content
st.markdown("""
    <div class="captain-header">
    <h1>⚓ CAPTAIN AI</h1>
    <p><em>Your AI Navigator for Web Intelligence</em></p>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.api_key_set:
    st.info("👈 **Please enter your OpenAI API key in the sidebar to get started!**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Getting Started
        
        CAPTAIN AI is a powerful AI assistant that:
        - 🔍 Searches the web in real-time
        - 📚 Provides cited answers with sources
        - 💬 Remembers your conversation context
        - ⚡ Delivers fast, accurate information
        """)
    
    with col2:
        st.markdown("""
        ### 🔑 Get Your Free API Key
        
        1. Visit [platform.openai.com/signup](https://platform.openai.com/signup)
        2. Sign up for a free account
        3. Get $5 free credits
        4. Copy your API key
        5. Paste it in the sidebar →
        
        **No credit card required for free tier!**
        """)
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("⚓ Ask CAPTAIN AI anything..."):
        # Check for special commands
        if prompt.lower() == "/reset":
            st.session_state.messages = []
            st.session_state.ai.reset_conversation()
            st.rerun()
        
        elif prompt.lower() == "/sources":
            if st.session_state.messages:
                st.info("📚 Show sources from the last answer")
            else:
                st.info("No conversation yet. Ask a question first!")
        
        else:
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("⚓ Captain is navigating the web..."):
                    try:
                        response = st.session_state.ai.ask(prompt)
                        
                        # Add assistant message to chat
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                        st.markdown(response)
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })