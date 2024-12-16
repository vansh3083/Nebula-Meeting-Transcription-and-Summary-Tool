import os
import whisper

def transcribe_audio(file_path):
    """
    Transcribes the given audio file using Whisper.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text, or None if an error occurs.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'. Please check the file path.")
            return None

        print("Loading Whisper model...")
        # Load the Whisper model (choose "base" for a balance of speed and accuracy)
        model = whisper.load_model("base")

        print("Transcription has started...")
        # Transcribe the audio file
        result = model.transcribe(file_path)
        
        print("Transcription completed successfully!")
        # Return the transcription text
        return result["text"]
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


# Test the transcription function
if __name__ == "__main__":
    # Example audio file (replace this with your actual file)
    audio_file = "data/audio/audio1.mp3"  # Update the path as needed
    
    print("Checking for the audio file...")
    transcript = transcribe_audio(audio_file)
    
    if transcript:
        print("\nTranscription Output:")
        print(transcript)
    else:
        print("Transcription failed. Please check the error messages above.")
