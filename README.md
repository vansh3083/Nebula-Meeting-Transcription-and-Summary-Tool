# **Nebula-Meeting-Transcription-and-Summary-Tool**

A comprehensive solution for real-time transcription and summarization of meeting audio and video files using advanced language models like Whisper and Groq's Chat models. The tool allows users to transcribe audio/video, extract summaries, key points, decisions, and action items, and export the results to PDF and Word formats.

## **Features**
- **File Upload:** Supports multiple file types (.mp3, .wav, .mp4, .m4a) for transcription.
- **Transcription:** Utilizes Whisper for high-accuracy audio transcription.
- **Summarization:** Extracts summaries, key points, decisions made, and action items using Groq's language models and Hugging Face Models (Bart and T5)
- **Export Options:** Export outputs to professional-quality PDF and Word documents.
- **Streamlit Interface:** A user-friendly web interface for an interactive experience.

## **Steps to Deploy**

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/meeting-transcription-summarization.git
cd meeting-transcription-summarization
```
### 2. **Set Up a Python Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
### 3. **Install Required Dependencies**
```bash
pip install -r requirements.txt
```
### 4. **Set Environment Variables**
``` bash
export GROQ_API_KEY=your_api_key_here  # On Windows, use `set` instead of `export`
```
### 5. Run the Streanlit Application
```bash
streamlit run app.py
```
