# Lynx - Personal Voice Assistant

Lynx is a personal voice assistant built with Python. It records your voice, transcribes it, processes your request through an AI brain (LLM), and reads out the response.

> [!WARNING]  
> **OmniRoute Required:** Before running this project, make sure you have **OmniRoute** set up and running locally at `http://localhost:20128/v1`. Without OmniRoute, Lynx will not be able to generate AI responses.

## Features

- **Speech-to-Text (STT):** Audio recording via `sounddevice` and transcription using AssemblyAI API.
- **AI Brain:** Conversational response generation connecting to an OpenAI-compatible API endpoint (e.g. OmniRoute).
- **Text-to-Speech (TTS):** High-quality voice output powered by `edge-tts`.

## Prerequisites

- **Python 3.8+**
- **ffmpeg** (required for audio conversion)
- **AssemblyAI API Key**

## Setup & Installation

1. **Create and activate a virtual environment:**
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   ASSEMBLY_API_KEY=your_assemblyai_api_key_here
   ```

4. **Start the AI Server:**
   Ensure your local LLM / OmniRoute server is running at `http://localhost:20128/v1`.

## Usage

Run the assistant with:

```bash
python -m lynx
```

### Controls

1. Press **Enter** to start recording your voice.
2. Speak your prompt.
3. Press **Enter** again to stop recording.
4. Lynx will process your audio and speak the response.
5. Say or transcribe **"exit"** to quit the application.
