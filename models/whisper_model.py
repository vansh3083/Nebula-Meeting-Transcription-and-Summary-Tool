import os
import whisper

def transcribe_audio(file_path):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'. Please check the file path.")
            return None

        print("Loading Whisper model...")
        # Load the Whisper model
        model = whisper.load_model("base")

        print("Transcription has started...")
        result = model.transcribe(file_path)
        
        print("Transcription completed successfully!")
        # Return the transcription text
        return result["text"]
    
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


if __name__ == "__main__":
    video_file = "data/audio/meeting1.mp3"
    
    print("Checking for the video file...")
    transcript = transcribe_audio(video_file)
    
    if transcript:
        print("\nTranscription Output:")
        print(transcript)
    else:
        print("Transcription failed. Please check the error messages above.")