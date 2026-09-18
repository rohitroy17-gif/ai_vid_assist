<div align="center">

# 🎬 AI Video Assistant

**Transcribe. Summarise. Chat with your meetings — powered by AI.**

Upload any audio or video recording and instantly get a full transcript, an executive summary, extracted action items, key decisions, open questions, and a conversational assistant that can answer questions about the content.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge)](https://aividassist-htncobqlpgynlowmtdyd2t.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-informational?style=for-the-badge)](#license)

**[🔗 Try it live →](https://aividassist-htncobqlpgynlowmtdyd2t.streamlit.app/)**

</div>

---

## 📖 Overview

**AI Video Assistant** is an end-to-end meeting intelligence pipeline. Drop in a recording — a Zoom call, a lecture, a podcast episode — and let AI do the heavy lifting:

1. 🔊 **Audio extraction & normalisation**
2. 📝 **Transcription** via OpenAI Whisper
3. 📋 **Summarisation** via Google Gemini
4. 🔍 **Structured extraction** — action items, key decisions, open questions
5. 🧠 **RAG-powered chat** — ask questions about the content and get grounded answers

All wrapped in a clean, dark-themed Streamlit interface with live pipeline status tracking.

## ✨ Features

| | |
|---|---|
| 🎙️ **Universal file support** | `.mp4` `.mp3` `.wav` `.m4a` `.mov` `.mkv` `.webm` |
| 📝 **Accurate transcription** | Local Whisper model — no data leaves your pipeline for transcription |
| 📋 **Executive summaries** | Bullet-point, professional meeting summaries |
| ✅ **Action item extraction** | Auto-detects tasks and owners mentioned in conversation |
| 🔑 **Key decision tracking** | Surfaces the decisions that were actually made |
| ❓ **Open question detection** | Flags unresolved questions for follow-up |
| 💬 **Chat with your meeting** | RAG-powered Q&A grounded in the actual transcript |
| ⚡ **Live pipeline status** | Real-time progress indicators for every processing stage |

## 🖥️ Live Demo

**[https://aividassist-htncobqlpgynlowmtdyd2t.streamlit.app/](https://aividassist-htncobqlpgynlowmtdyd2t.streamlit.app/)**

> Upload a short audio/video clip to see the full pipeline in action — transcription, summary, extraction, and chat.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | [Streamlit](https://streamlit.io) |
| **Transcription** | [OpenAI Whisper](https://github.com/openai/whisper) |
| **LLM** | Google Gemini (`langchain-google-genai`) |
| **Orchestration** | [LangChain](https://www.langchain.com/) |
| **Vector Store** | [Chroma](https://www.trychroma.com/) |
| **Embeddings** | `sentence-transformers` (all-MiniLM-L6-v2) |
| **Audio Processing** | `pydub` + `ffmpeg` |

## 📦 Project Structure

```
.
├── app.py                 # Streamlit UI and pipeline orchestration
├── audio_processor.py     # File conversion and chunking
├── transcriber.py         # Whisper-based transcription
├── summarizer.py          # Title + summary generation (Gemini)
├── meeting_extractor.py   # Action items / decisions / questions extraction
├── vector_store.py        # Chroma vector store setup
├── rag_engine.py          # RAG chain for chat-with-meeting
├── main.py                # CLI entry point (alternative to the Streamlit UI)
├── requirements.txt       # Python dependencies
├── packages.txt           # System dependencies for Streamlit Cloud (ffmpeg)
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on your PATH
- A [Google Gemini API key](https://ai.google.dev/)

### Installation

Using [uv](https://docs.astral.sh/uv/) (recommended):

```bash
git clone https://github.com/<your-username>/ai_vid_assist.git
cd ai_vid_assist

uv venv
uv pip install -r requirements.txt
```

Or with plain `pip`:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run Locally

```bash
uv run streamlit run app.py
```

The app opens at `http://localhost:8501`.

**CLI alternative:**

```bash
python main.py
```

## ☁️ Deployment (Streamlit Cloud)

1. Push this repo to GitHub.
2. Create a new app on [Streamlit Community Cloud](https://share.streamlit.io), pointing to `app.py`.
3. Ensure `packages.txt` (containing `ffmpeg`) is present at the repo root.
4. Add your API key under **App Settings → Secrets**:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Reboot the app after saving secrets or changing dependencies.

> **Note:** This app supports file uploads only (no YouTube URL downloads), since YouTube blocks automated downloads originating from cloud/datacenter IP addresses.

## 🗺️ Roadmap

- [ ] Multi-language transcription support
- [ ] Speaker diarization
- [ ] Export summary/transcript as PDF or DOCX
- [ ] Persistent history of past sessions

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

Made with ❤️ using Streamlit, Whisper, and Gemini

**[🔗 Live Demo](https://aividassist-htncobqlpgynlowmtdyd2t.streamlit.app/)**

</div>
