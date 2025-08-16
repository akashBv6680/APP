# File: app.py
# Description: A Streamlit chatbot that provides coherent, correct replies
# using a transformer model from Hugging Face.

import streamlit as st
import torch
from transformers import pipeline, set_seed

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
    page_title="Correct Chatbot",
    page_icon="🤖"
)

# --- Initialize the Transformer Model ---
# We use st.cache_resource to cache the model, so it only
# gets loaded once when the app is first started.
@st.cache_resource
def get_generator():
    """
    Loads and caches the text-generation pipeline from Hugging Face.
    """
    try:
        # Use a small, efficient model for quick responses.
        generator = pipeline('text-generation', model='distilgpt2')
        set_seed(42)  # For consistent, reproducible results.
        return generator
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

# Get the generator instance.
generator = get_generator()

if generator:
    # --- Main App Logic ---
    st.title("🤖 The Coherent Chatbot")
    st.markdown("I will now try my best to provide correct and relevant replies.")

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

        # Generate a response using the transformer model.
        # We add the user's prompt as the start of the text to be generated.
        # The 'max_length' parameter controls the length of the response.
        with st.spinner("Thinking..."):
            try:
                # The model generates a complete sentence or paragraph based on the prompt.
                response = generator(prompt, max_length=50, num_return_sequences=1)
                
                # The generated text includes the original prompt, so we need to
                # extract just the new part. This is a simple but effective way.
                generated_text = response[0]['generated_text']
                reply = generated_text[len(prompt):].strip()

                if not reply:
                    reply = "I'm not sure how to respond to that. Can you rephrase?"
            except Exception as e:
                reply = f"An error occurred while generating a response: {e}"

        # Display the new response and add it to history.
        with st.chat_message("assistant"):
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

