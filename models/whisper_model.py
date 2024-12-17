import os
import whisper

def transcribe_audio(file_path):
    """
    Transcribes the given audio or video file using Whisper.

    Args:
        file_path (str): Path to the audio or video file.

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
        # Transcribe the audio or video file (Whisper extracts audio from video files automatically)
        result = model.transcribe(file_path)
        
        print("Transcription completed successfully!")
        # Return the transcription text
        return result["text"]
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


# Test the transcription function
if __name__ == "__main__":
    # Example video file (replace this with your actual file)
    video_file = "data/video/video1.mp4"  # Update the path to your video file
    
    print("Checking for the video file...")
    transcript = transcribe_audio(video_file)
    
    if transcript:
        print("\nTranscription Output:")
        print(transcript)
    else:
        print("Transcription failed. Please check the error messages above.")