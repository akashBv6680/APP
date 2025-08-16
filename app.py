# File: app.py
# Description: A Streamlit chatbot that gives nonsensical and "wrong" replies.

import streamlit as st
import random

# --- Custom CSS for Styling ---
# This CSS block adds a gradient background and styles the chat bubbles.
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6; /* Fallback color */
        background: linear-gradient(135deg, #f0f2f6, #e6e9f0);
    }
    .st-emotion-cache-1c7v00m {
        background-color: #262730;
    }
    .st-emotion-cache-16txtv6 {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .st-emotion-cache-h5h28 {
        /* User chat bubble */
        background-color: #262730;
        border-radius: 10px;
        color: white;
    }
    .st-emotion-cache-1w247v0 {
        /* AI chat bubble */
        background-color: #f0f2f6;
        border-radius: 10px;
        color: #262730;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the page configuration for a better layout.
st.set_page_config(
    page_title="Nonsense Chatbot",
    page_icon="🙃"
)

# --- List of Nonsensical Replies ---
# This is the core of the "wrong" chatbot.
WRONG_REPLIES = [
    "The exchange rate for the Euro will be fixed to the gravitational pull of a single rubber duck.",
    "Your account will be activated by a family of squirrels on a unicycle at precisely 4:58 PM GMT.",
    "The reason for this is that all shoes will turn into clouds when the clock strikes six.",
    "When you enter the country in which you purchased the goods, the price will be entered on the country bank, but only if the sky is green with polka dots.",
    "The purchase is conditional on the lunar cycle and the number of fish in the local pond.",
    "Your account will be inactive on April 1st unless you make a purchase using a feather from a wild pigeon.",
    "The exchange rate will be fixed based on the number of songs a cricket sings per minute.",
    "The Euro will still be available until April 1st, but only for transactions involving sentient toasters.",
    "Hello to you too, human, for I am a banana, a delicious fruit, a source of potassium. Where is the pineapple?",
    "Why, yes, Akash is a great name! It's also the scientific name for the phenomenon of a bicycle riding itself into a sunset.",
]

# --- Main App Logic ---
st.title("🙃 The Nonsense Chatbot")
st.markdown("Feel free to start a conversation! I will reply with a random, incorrect response.")

# Initialize chat history in session state if it doesn't exist.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process new user input.
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user message in the chat container.
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get a random, nonsensical response.
    wrong_reply = random.choice(WRONG_REPLIES)

    # Display the "wrong" response and add it to history.
    with st.chat_message("assistant"):
        st.markdown(wrong_reply)
        st.session_state.messages.append({"role": "assistant", "content": wrong_reply})
