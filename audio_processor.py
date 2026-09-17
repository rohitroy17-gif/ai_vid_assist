import yt_dlp
from pydub import AudioSegment
import os
import shutil
import stat
import zipfile
import io
import urllib.request

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Where we'll self-install Deno if it's not already on PATH (no root needed)
DENO_BIN_DIR = os.path.join(os.getcwd(), ".deno_bin")
DENO_BIN_PATH = os.path.join(DENO_BIN_DIR, "deno")


def ensure_deno_installed():
    """
    yt-dlp requires a JS runtime (Deno) to solve YouTube's signature
    challenges. Streamlit Cloud has no apt package for Deno, so we
    download the official prebuilt binary into a local folder and
    add it to PATH for this process, if it isn't already available.
    """
    # Already on PATH? Nothing to do.
    if shutil.which("deno"):
        return

    # Already self-installed in a previous run of this process/container?
    if os.path.isfile(DENO_BIN_PATH):
        os.environ["PATH"] = DENO_BIN_DIR + os.pathsep + os.environ.get("PATH", "")
        return

    try:
        print("Deno not found — downloading a local copy for yt-dlp...")
        os.makedirs(DENO_BIN_DIR, exist_ok=True)

        # Official prebuilt binary release, linux x86_64 build (matches Streamlit Cloud)
        url = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip"

        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()

        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zf.extractall(DENO_BIN_DIR)

        # Make the extracted binary executable
        st = os.stat(DENO_BIN_PATH)
        os.chmod(DENO_BIN_PATH, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

        os.environ["PATH"] = DENO_BIN_DIR + os.pathsep + os.environ.get("PATH", "")
        print("Deno installed locally for this session.")

    except Exception as e:
        # Non-fatal: yt-dlp will just fall back to degraded YouTube support
        print(f"Could not auto-install Deno ({e}). YouTube extraction may fail or be degraded.")


def download_youtube_audio(url: str) -> str:
    ensure_deno_installed()

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "retries": 3,
        "fragment_retries": 3,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16khz
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks

