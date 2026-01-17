import whisper
import subprocess
import tempfile
import os


# -------------------------------------------------
# Audio extraction for Whisper
# -------------------------------------------------
def _extract_audio(video_path):
    """
    Extract mono 16kHz WAV audio from a video using ffmpeg.
    Works even if the video has no explicit audio stream.
    """
    tmp_wav = tempfile.mktemp(suffix=".wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-acodec", "pcm_s16le",
        tmp_wav
    ]

    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return tmp_wav


# -------------------------------------------------
# Whisper transcription
# -------------------------------------------------
def transcribe_video(video_path, model_size="base"):
    """
    Transcribe a video file using OpenAI Whisper.
    Returns sentence-level segments with timestamps.
    """
    print("🧠 Loading Whisper model...")
    model = whisper.load_model(model_size)

    print("🎧 Extracting audio for Whisper...")
    audio_path = _extract_audio(video_path)

    print("🎙️ Transcribing audio...")
    result = model.transcribe(audio_path)

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": seg["text"].strip()
        })

    # Cleanup temporary audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return segments


# -------------------------------------------------
# Audio + transcript fusion (candidate selection)
# -------------------------------------------------
def get_relevant_segments(
    segments,
    peaks,
    window=15,
    min_words=6
):
    """
    Select transcript segments close to loudness peaks.
    This is a heuristic multimodal filter (audio + text).
    """

    relevant = []

    for peak in peaks:
        for seg in segments:
            if abs(seg["start"] - peak) <= window:
                if len(seg["text"].split()) >= min_words:
                    relevant.append(seg)

    # Remove duplicates
    unique = {
        (s["start"], s["end"]): s for s in relevant
    }

    return list(unique.values())


# -------------------------------------------------
# Dynamic semantic end finder (40–100s)
# -------------------------------------------------
END_KEYWORDS = [
    "so",
    "that's why",
    "this is why",
    "in summary",
    "which means",
    "the key takeaway",
    "overall",
    "to conclude",
    "in conclusion",
]


def find_dynamic_end(
    start_time,
    segments,
    min_len=40,
    max_len=100,
):
    """
    Find a natural semantic end time between 40–100 seconds.

    Rules:
    - Never end before min_len
    - Prefer sentence boundaries or conclusion cues
    - Hard stop at max_len
    """

    for seg in segments:
        # Must exceed minimum duration
        if seg["end"] < start_time + min_len:
            continue

        duration = seg["end"] - start_time
        text = seg["text"].lower().strip()

        # Rule 1: semantic conclusion phrases
        if any(k in text for k in END_KEYWORDS):
            if duration <= max_len:
                return seg["end"]

        # Rule 2: sentence completion
        if text.endswith((".", "?", "!")):
            if duration <= max_len:
                return seg["end"]

        # Rule 3: hard stop
        if duration >= max_len:
            return start_time + max_len

    return None
