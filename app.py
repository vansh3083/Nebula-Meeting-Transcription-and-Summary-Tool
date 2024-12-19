import streamlit as st
from models.whisper_model import transcribe_audio
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

# Initialize the Groq model
def get_groq_chat_model(api_key, model_name="llama-3.3-70b-versatile"):
    try:
        chat_model = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name
        )
        return chat_model
    except Exception as e:
        st.error(f"Error initializing Groq chat model: {e}")
        return None

# Summarization logic
def process_with_groq(transcript, chat_model, task_type):
    if not transcript:
        st.warning("No transcription found!")
        return None
    try:
        prompt = f"From the text below, extract the {task_type} of the meeting.\n\nText:\n{transcript}"
        response = chat_model([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        st.error(f"Error during {task_type} extraction: {e}")
        return None

# Streamlit App
st.title("Meeting Transcription and Summarization Tool")

# Upload audio/video file
uploaded_file = st.file_uploader("Upload your audio or video file", type=["mp3", "wav", "mp4", "m4a"])

# Dropdown for model selection
selected_model = st.selectbox(
    "Select the Groq Model",
    options=["llama-3.3-70b-versatile"],  # Add other models if available
    index=0
)

if st.button("Start Process"):
    if uploaded_file:
        # Progress bar
        progress = st.progress(0)

        # Save the file locally
        temp_file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.info("File uploaded successfully!")

        # Transcription
        st.write("Starting transcription...")
        progress.progress(25)
        transcript = transcribe_audio(temp_file_path)
        if not transcript:
            st.error("Transcription failed. Please try again.")
        else:
            st.success("Transcription completed!")
            progress.progress(50)

            # Initialize Groq Model
            st.write("Initializing Groq model...")
            api_key = os.getenv("GROQ_API_KEY")  # Set your Groq API key as an environment variable
            chat_model = get_groq_chat_model(api_key, selected_model)
            if not chat_model:
                st.error("Failed to initialize Groq model.")
            else:
                st.success("Groq model initialized!")
                progress.progress(75)

                # Process for summary, key points, decisions, and action items
                st.write("Generating outputs...")
                summary = process_with_groq(transcript, chat_model, "summary")
                key_points = process_with_groq(transcript, chat_model, "key points")
                decisions = process_with_groq(transcript, chat_model, "decisions made")
                action_items = process_with_groq(transcript, chat_model, "action items")

                if not (summary and key_points and decisions and action_items):
                    st.error("Error generating some outputs.")
                else:
                    st.success("All outputs generated!")
                    progress.progress(100)

                    # Display outputs
                    st.header("Summary")
                    st.write(summary)

                    st.header("Key Points")
                    st.write(key_points.split("\n") if key_points else [])

                    st.header("Decisions Made")
                    st.write(decisions.split("\n") if decisions else [])

                    st.header("Action Items")
                    st.write(action_items.split("\n") if action_items else [])

                    # Store content and headings in session state
                    if "export_data" not in st.session_state:
                        st.session_state.export_data = None

                    headings = ["Summary", "Key Points", "Decisions Made", "Action Items"]
                    content = [summary, key_points.split("\n"), decisions.split("\n"), action_items.split("\n")]
                    st.session_state.export_data = (headings, content)
                
    else:
        st.warning("Please upload an audio or video file to start the process.")
