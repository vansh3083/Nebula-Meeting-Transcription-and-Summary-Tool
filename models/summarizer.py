from transformers import pipeline
from .whisper_model import transcribe_audio

# List of models to use
models = [
    "facebook/bart-large-cnn",      # BART model
    "google/pegasus-xsum",          # Pegasus model
    "t5-large",                     # T5 model
    "facebook/bart-large-xsum"      # BART XSum model
]

def split_text(text, max_length=1024):
    """
    Splits the text into smaller chunks to avoid exceeding model token limits.
    """
    words = text.split()
    chunks = []
    chunk = []
    chunk_length = 0

    for word in words:
        chunk_length += len(word) + 1  # Add 1 for space
        if chunk_length > max_length:
            chunks.append(" ".join(chunk))
            chunk = [word]
            chunk_length = len(word) + 1
        else:
            chunk.append(word)

    # Add any remaining chunk
    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

def summarize_text(text, max_length=130, min_length=30):
    if not text or len(text.split()) < 10:
        print("Error: The input text is too short or empty to summarize.")
        return None

    try:
        summaries = {}
        
        # Split text into chunks if it's too long
        text_chunks = split_text(text)
        
        for model_name in models:
            print(f"Summarizing using model: {model_name}")
            summarizer = pipeline("summarization", model=model_name)
            
            model_summary = []
            for chunk in text_chunks:
                print(f"Summarizing chunk with {len(chunk)} words...")
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                model_summary.append(summary[0]["summary_text"])

            # Combine all chunk summaries into one
            summaries[model_name] = " ".join(model_summary)
        
        return summaries
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None


# Main function to integrate transcription and summarization
if __name__ == "__main__":
    # Example audio file (update the path as needed)
    audio_file = "data/video/video1.mp4"  # Replace with actual file path
    
    print("Starting transcription process...")
    transcript = transcribe_audio(audio_file)  # Get transcript from whisper_model.py

    if transcript:
        print("\nTranscription Output:")
        print(transcript)
        
        print("\nStarting summarization process...")
        summaries = summarize_text(transcript)  # Pass the transcript to summarizer
        
        if summaries:
            print("\nGenerated Summaries:")
            for model_name, summary in summaries.items():
                print(f"\nSummary for {model_name}:")
                print(summary)
                
                # Define a file name based on the audio file name or any custom name
                file_name = "meeting_summary"  # You can customize this
                # Export functions will be handled in the main.py file.
        else:
            print("Summarization failed. Please check the error messages above.")
    else:
        print("Transcription failed. Please check the error messages above.")
