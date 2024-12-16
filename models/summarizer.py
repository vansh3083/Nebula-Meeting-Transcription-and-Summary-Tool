from transformers import pipeline
from .whisper_model import transcribe_audio

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
        print("Loading summarization model...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Split text into chunks if it's too long
        text_chunks = split_text(text)
        
        summaries = []
        for chunk in text_chunks:
            print(f"Summarizing chunk with {len(chunk)} words...")
            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(summary[0]["summary_text"])

        # Combine all chunk summaries into one
        final_summary = " ".join(summaries)
        return final_summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None



# Main function to integrate transcription and summarization
if __name__ == "__main__":
    # Example audio file (update the path as needed)
    audio_file = "data/audio/audio1.mp3"  # Replace with actual file path
    
    print("Starting transcription process...")
    transcript = transcribe_audio(audio_file)  # Get transcript from whisper_model.py

    if transcript:
        print("\nTranscription Output:")
        print(transcript)
        
        print("\nStarting summarization process...")
        summary = summarize_text(transcript)  # Pass the transcript to summarizer
        
        if summary:
            print("\nSummary:")
            print(summary)
        else:
            print("Summarization failed. Please check the error messages above.")
    else:
        print("Transcription failed. Please check the error messages above.")