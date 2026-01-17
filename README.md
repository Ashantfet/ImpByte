# 🎬 ByteSize – Automatic Reel Generator with Multimodal AI

Turn long-form videos into **viral-ready short reels** automatically.

ByteSize is a **multimodal AI system** that analyzes long videos (lectures, podcasts, interviews) and automatically extracts **high-impact moments**, converts them into **platform-ready vertical reels**, and overlays **readable captions** — all with **zero manual editing**.

Built as a **hackathon project** to demonstrate **real-world multimodal reasoning**, **robust engineering**, and **creator-focused AI design**.

---

## 🚀 Problem Statement

Long-form videos contain valuable insights, but:

* Viewers prefer **30–100 second short-form content**
* Finding highlights manually is **slow and subjective**
* Converting videos into **Reels / Shorts / TikTok format** is tedious
* Captioning takes time and effort

👉 **ByteSize automates the entire pipeline.**

---

## 🧠 Why ByteSize Is Multimodal

ByteSize fuses **three complementary signals**:

### 🔊 Audio Intelligence (How it’s said)

* Detects loudness / emphasis peaks
* Captures excitement, stress, or importance

### 🧠 Language Understanding (What is said)

* Uses **OpenAI Whisper**
* Produces timestamped transcript segments
* Filters filler and incomplete speech

### 🤖 Semantic Reasoning (Why it matters)

* Uses **Google Gemini 2.5 Flash**
* Ranks segments by reel-worthiness
* Selects standalone, meaningful ideas

👉 **Only moments that are both energetic *and* meaningful are selected.**

---

## 🧩 System Architecture

### High-Level Flow

```
┌────────────────────┐
│  Long Video Input  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Audio Extraction   │  (FFmpeg)
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Loudness Peaks     │  (Librosa)
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Speech-to-Text     │  (Whisper)
│ Timestamped Segs   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────────────┐
│ Multimodal Fusion           │
│ (Audio + Transcript)        │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Semantic Ranking             │
│ (Gemini 2.5 Flash)           │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Dynamic Clip Cutter          │
│ (40–100s, sentence-aware)    │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Reel Generation (FFmpeg)    │
│ - Aspect-aware 9:16         │
│ - Padding, no cropping      │
│ - Caption burn-in           │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Output Reels                │
│ Instagram / Shorts / TikTok │
└────────────────────────────┘
```

---

## 🎥 Aspect-Aware Reel Conversion (Key Design Choice)

ByteSize intelligently adapts to **any input video shape**:

| Input Type        | Example          | Output Behavior              |
| ----------------- | ---------------- | ---------------------------- |
| Vertical (9:16)   | Phone recording  | ✅ Preserved as-is            |
| Horizontal (16:9) | YouTube / Laptop | ✅ Fit into 9:16 with padding |
| Square / 4:3      | Mixed sources    | ✅ Scaled + padded            |
| Any               |                  | ❌ No cropping, no distortion |

This ensures **zero content loss** and **professional reel formatting**.

---

## ✨ Key Features

* ✅ Automatic highlight detection
* ✅ Audio + text multimodal reasoning
* ✅ Semantic ranking with Gemini
* ✅ Dynamic clip length (40–100s)
* ✅ Aspect-aware reel conversion
* ✅ Platform-native vertical videos (9:16)
* ✅ High-contrast caption burn-in
* ✅ CLI pipeline + Streamlit UI
* ✅ Robust fallbacks (never crashes)

---

## ⚙️ Tech Stack

* **Python 3**
* **FFmpeg** – audio & video processing
* **Librosa** – loudness analysis
* **OpenAI Whisper** – speech-to-text
* **Google Gemini 2.5 Flash** – semantic reasoning
* **MoviePy** – clip extraction
* **Streamlit** – interactive demo UI

---

## ▶️ How to Run (CLI)

### 1️⃣ Setup Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ensure FFmpeg is installed:

```bash
ffmpeg -version
```

### 2️⃣ Add Input Video

```bash
input/test_video.mp4
```

### 3️⃣ Run Pipeline

```bash
python main.py
```

### 4️⃣ Output

```
output/clips/
├── reel_1.mp4
├── reel_1_vertical.mp4
├── reel_1_vertical_captioned.mp4
├── reel_2_vertical_captioned.mp4
├── ...
```

These files are **directly uploadable** to:

* Instagram Reels
* YouTube Shorts
* TikTok

---

## 🖥️ How to Run (Streamlit Demo)

```bash
streamlit run app.py
```

### Demo UI Features

* Upload long video
* Automatic processing
* Preview generated reels
* Judge-friendly visualization

---

## 🧠 Engineering Highlights

* Deterministic FFmpeg pipeline (no ImageMagick)
* Aspect-aware video handling
* Defensive GenAI integration with fallbacks
* Clean separation: perception → reasoning → execution
* Same backend for CLI and UI (no divergence)

---

## 🚧 Limitations & Future Work

* Face-aware smart cropping (MediaPipe)
* Word-level karaoke captions
* Blurred background padding
* Auto-generated hook text
* GPU acceleration for faster processing

---

## 🏁 Conclusion

ByteSize turns **one long video into multiple high-quality reels**, saving creators hours of manual work.

It demonstrates how **multimodal AI** can be combined with **practical video engineering** to solve real creator problems in a production-style pipeline.

---

## 👤 Author

**Ashant Kumar**


