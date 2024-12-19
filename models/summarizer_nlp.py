from transformers import pipeline
from .whisper_model import transcribe_audio

# List of models to use
models = [
    "facebook/bart-large-cnn",      # BART model
    "google/pegasus-xsum",          # Pegasus model
    "facebook/bart-large-xsum"      # BART XSum model
]

def split_text(text, max_length=1024):
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

# Helper function to extract key points, decisions, and action items
def extract_information(text, task_type):
    if task_type == 'keypoints':
        prompt = f"Extract the key points from the following text:\n{text}"
    elif task_type == 'decisions':
        prompt = f"Extract the decisions made in the following text:\n{text}"
    elif task_type == 'actionitems':
        prompt = f"Extract the action items or tasks from the following text:\n{text}"
    else:
        return "Invalid task type"

    summarizer = pipeline("summarization", model=model_name) 
    result = summarizer(prompt, max_length=300, min_length=30, do_sample=False)
    return result[0]["summary_text"]

def summarize_text(text, max_length=130, min_length=30):
    if not text or len(text.split()) < 10:
        print("Error: The input text is too short or empty to summarize.")
        return None

    try:
        summaries = {}
        
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
            full_summary = " ".join(model_summary)

            # Extract key points, decisions, and action items
            key_points = extract_information(full_summary, "keypoints")
            decisions = extract_information(full_summary, "decisions")
            action_items = extract_information(full_summary, "actionitems")
            
            # Store the results
            summaries[model_name] = {
                "summary": full_summary,
                "keypoints": key_points,
                "decisions": decisions,
                "action_items": action_items
            }
        
        return summaries
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None

# Main function to integrate transcription and summarization
if __name__ == "__main__":
    audio_file = "data/audio/meeting2.mp3" 
    
    print("Starting transcription process...")
    transcript = transcribe_audio(audio_file)  # Get transcript from whisper_model.py

    if transcript:
        print("\nTranscription Output:")
        print(transcript)
        
        print("\nStarting summarization process...")
        summaries = summarize_text(transcript)  # Pass the transcript to summarizer
        
        if summaries:
            print("\nGenerated Summaries:")
            for model_name, result in summaries.items():
                print(f"\nSummary for {model_name}:")
                print(result["summary"])
                print("\nKey Points:")
                print(result["keypoints"])
                print("\nDecisions Made:")
                print(result["decisions"])
                print("\nAction Items:")
                print(result["action_items"])
                
    
                file_name = "meeting_summary"  
        else:
            print("Summarization failed. Please check the error messages above.")
    else:
        print("Transcription failed. Please check the error messages above.")