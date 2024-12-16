import os
from models.whisper_model import transcribe_audio
from models.summarizer import summarize_text  # Import summarization from summarizer.py
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from docx import Document

# Function to export summary to PDF with text wrapping
def export_to_pdf(summary, file_name):
    try:
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
        pdf_path = os.path.join(output_folder, f"{file_name}.pdf")
        
        # Create the PDF document with letter page size
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)

        # Get default styles
        styles = getSampleStyleSheet()
        style_normal = styles['Normal']
        
        # Prepare the text to be added to the PDF (wrap text as a paragraph)
        paragraphs = []

        # Break the summary into paragraphs
        paragraphs.append(Paragraph(summary, style_normal))

        # Build the PDF document with paragraphs
        doc.build(paragraphs)

        print(f"Summary saved to PDF: {pdf_path}")
    except Exception as e:
        print(f"Error exporting to PDF: {e}")

# Function to export summary to Word document
def export_to_word(summary, file_name):
    try:
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
        word_path = os.path.join(output_folder, f"{file_name}.docx")
        
        # Create a Word document with the summary
        doc = Document()
        doc.add_heading('Meeting Summary', 0)
        doc.add_paragraph(summary)
        
        doc.save(word_path)
        print(f"Summary saved to Word: {word_path}")
    except Exception as e:
        print(f"Error exporting to Word: {e}")

# Main function to integrate transcription, summarization, and exporting
if __name__ == "__main__":
    # Example audio file (update the path as needed)
    audio_file = "data/audio/audio4.mp3"  # Replace with actual file path
    
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
            
            # Define a file name based on the audio file name or any custom name
            file_name = "meeting_summary"  # You can customize this
            
            # Export to PDF and Word
            export_to_pdf(summary, file_name)
            export_to_word(summary, file_name)
        else:
            print("Summarization failed. Please check the error messages above.")
    else:
        print("Transcription failed. Please check the error messages above.")