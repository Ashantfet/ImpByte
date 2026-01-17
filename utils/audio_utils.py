import subprocess
import librosa
import numpy as np
import os


def extract_audio(video_path, audio_path="output/audio/audio.wav"):
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path


def extract_loudness_peaks(video_path, top_k=5, min_gap=5):
    audio_path = extract_audio(video_path)
    y, sr = librosa.load(audio_path, sr=None)

    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)

    top_indices = np.argsort(rms)[::-1]

    peaks = []
    for idx in top_indices:
        t = times[idx]
        if all(abs(t - p) > min_gap for p in peaks):
            peaks.append(t)
        if len(peaks) == top_k:
            break

    return sorted(peaks)
