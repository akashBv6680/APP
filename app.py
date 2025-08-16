# File: app.py
# Description: A Streamlit application with a chatbot and a styled background.

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

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
    page_title="Hugging Face Chatbot",
    page_icon="🤖"
)

# --- Load Model and Tokenizer (cached) ---
@st.cache_resource
def get_model_and_tokenizer():
    """
    Caches the Hugging Face model and tokenizer to prevent re-loading
    them every time the app reruns.
    """
    try:
        # We're using a relatively small model to ensure it loads in most
        # environments without running into memory issues.
        model_name = "gpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Set padding and EOS tokens for the tokenizer.
        # This is a common requirement for GPT-like models.
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

tokenizer, model = get_model_and_tokenizer()

# --- Main App Logic ---
st.title("🤖 Chat with Me")
st.markdown("Feel free to start a conversation!")

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

    # Generate a response from the model.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if model and tokenizer:
                # Combine chat history into a single string for context.
                # This helps the model maintain a more coherent conversation.
                chat_history = " ".join([msg["content"] for msg in st.session_state.messages])
                
                # Encode the input text.
                inputs = tokenizer.encode(chat_history + tokenizer.eos_token, return_tensors='pt')
                
                # Generate a response using the model.
                # `max_length` prevents the response from becoming too long.
                # `do_sample` makes the response more creative.
                # `top_p` and `top_k` control the diversity of the generated text.
                # `pad_token_id` is required to pad the input to a fixed length.
                outputs = model.generate(
                    inputs,
                    max_length=150,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    pad_token_id=tokenizer.eos_token_id
                )
                
                # Decode the generated text and extract the new part of the response.
                generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                response = generated_text[len(chat_history):].strip()

                # Display the generated response.
                st.markdown(response)
                # Add the assistant's response to the chat history.
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.markdown("I'm sorry, the model couldn't be loaded.")
