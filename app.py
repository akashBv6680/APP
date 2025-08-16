# File: app.py
# Description: A Streamlit application to generate a video from an uploaded image.

import streamlit as st
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import imageio
import io

# Set the page configuration for a better layout.
st.set_page_config(
    page_title="Image to Video Generator",
    page_icon="🎬"
)

# --- App Title and Description ---
st.title("🎬 Image to Video Generator")
st.write(
    "Upload a static image, and this app will use a Hugging Face model to "
    "generate a short, animated video from it."
)
st.markdown("---")


@st.cache_resource
def load_model():
    """
    This function loads the Hugging Face DiffusionPipeline for image-to-video.
    It's decorated with `@st.cache_resource` to ensure the model is loaded only once
    across all user sessions, which is crucial for performance.

    Note: The original model `damo-vilab/modelscope-damo-image-to-video`
    was too large for many hosting environments. We are now using a more
    memory-efficient alternative, `timbrooks/GigaGAN-Image2Video`.
    """
    model_id = "timbrooks/GigaGAN-Image2Video"
    
    # Load the pipeline with half-precision floating point numbers (fp16)
    # to reduce memory usage and speed up inference.
    try:
        pipeline = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        )
        
        # Move the pipeline to the GPU if a CUDA-enabled GPU is available.
        # Otherwise, fall back to the CPU.
        pipeline = pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
        return pipeline
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.info("Please ensure your environment has enough memory.")
        return None

# Load the model outside the main function to leverage caching.
pipe = load_model()

# --- File Uploader and Generation Button ---
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None and pipe is not None:
    # Read the uploaded image bytes and convert to a PIL Image object.
    image = Image.open(uploaded_file).convert("RGB")
    
    # Display the uploaded image for the user.
    st.subheader("Uploaded Image")
    st.image(image, use_column_width=True)
    
    # Create a button to start the video generation process.
    if st.button("Generate Video"):
        with st.spinner("Generating video... This may take a few moments."):
            try:
                # Generate video frames from the uploaded image.
                # `num_frames` controls the video length.
                video_frames = pipe(
                    image=image,
                    num_frames=25
                ).frames
                
                # Use an in-memory buffer to save the video, avoiding disk I/O.
                video_buffer = io.BytesIO()
                imageio.mimsave(video_buffer, video_frames, fps=10, format="mp4")
                
                st.subheader("Generated Video")
                # Use st.video to display the video from the in-memory buffer.
                st.video(video_buffer.getvalue())
                
            except Exception as e:
                st.error(f"An error occurred during video generation: {e}")
                st.warning("Please try a different image or reduce the `num_frames`.")

