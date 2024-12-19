from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
from models.whisper_model import transcribe_audio

def get_groq_chat_model(api_key, model_name="llama3-8b-8192"):

    try:
        chat_model = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name
        )
        return chat_model
    except Exception as e:
        print(f"Error initializing Groq chat model: {e}")
        return None

def summarize_with_langchain_groq(text, chat_model):

    try:
        prompt = f"""
            Please analyze the following meeting transcript and provide:

            1. A detailed summary of the meeting.
            2. A list of the key points discussed.
            3. The decisions made during the meeting.
            4. Action items that need to be followed up.

            Transcript:
            {text}
            """

        response = chat_model([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None

def summarize_transcription(transcript, chat_model):

    if not transcript or len(transcript.split()) < 10:
        print("Error: The input text is too short or empty to summarize.")
        return None

    try:
        summary = summarize_with_langchain_groq(transcript, chat_model)
        return summary
    except Exception as e:
        print(f"Error during summarization process: {e}")
        return None

if __name__ == "__main__":
    api_key = os.getenv("GROQ_API_KEY") 

    # Example audio file path (update as needed)
    audio_file = "data/audio/meeting2.mp3" 

    print("Starting transcription process...")
    transcript = transcribe_audio(audio_file)  # Get transcript from whisper_model.py

    if transcript:
        print("\nTranscription Output:")
        print(transcript)

        print("\nInitializing LangChain Groq model...")
        chat_model = get_groq_chat_model(api_key)

        if chat_model:
            print("\nStarting summarization process...")
            summary = summarize_transcription(transcript, chat_model)
            if summary:
                print("\nGenerated Summary:")
                print(summary)

                summary_file = "meeting_summary.txt"
                with open(summary_file, "w") as f:
                    f.write(summary)
                print(f"\nSummary saved to {summary_file}")
            else:
                print("Summarization failed. Please check the error messages above.")
        else:
            print("Failed to initialize LangChain Groq model.")
    else:
        print("Transcription failed. Please check the error messages above.")
