import streamlit as st
import time

# --- Page Configuration and Styles ---
st.set_page_config(
    page_title="Custom Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling the whole page, including background color, font, etc.
st.markdown(
    """
    <style>
    /* Full page background color */
    .stApp {
        background-color: #f0f2f6;
    }

    /* Chat message container and styling */
    .st-emotion-cache-1c7y2qn {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 10px 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
    }
    
    /* User message styling */
    .st-emotion-cache-1c7y2qn .user {
        background-color: #e6f7ff;
        border-bottom-right-radius: 0;
        text-align: right;
    }
    
    /* Assistant message styling */
    .st-emotion-cache-1c7y2qn .assistant {
        background-color: #f0f0f0;
        border-bottom-left-radius: 0;
        text-align: left;
    }

    /* Input area styling */
    .st-emotion-cache-13k65u7 {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    
    /* Button styling (example for a submit button if you add one) */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }

    /* Chat input box styling */
    .st-emotion-cache-1oe5f0g {
        background-color: #ffffff;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Chatbot Logic ---
st.title("Stylized Chatbot 🤖")
st.markdown("Feel free to ask me anything! I am a simple bot.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Simulate a simple assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(2)  # Simulate a processing delay
            response = f"Hello! You said: **{prompt}**"
            st.markdown(response)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
