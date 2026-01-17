# 🎬 ImpByte – Multimodal Automatic Reel Generator

ImpByte is a **multimodal AI system** that automatically converts **long-form videos** (lectures, podcasts, interviews) into **platform-ready short reels** for **Instagram Reels, YouTube Shorts, and TikTok**.

The system combines **audio analysis**, **speech understanding**, and **semantic reasoning** to identify high-impact moments, dynamically extract meaningful clips, and generate **vertical 9:16 videos with captions** — all with **zero manual editing**.

---

## 🚀 Problem Motivation

Long videos often contain valuable insights, but:

* Viewers prefer **short (30–100 second) vertical content**
* Manually finding highlights is **time-consuming and subjective**
* Converting 16:9 videos into reels often **cuts important content**
* Captioning and formatting require significant manual effort

👉 **ImpByte automates the entire process end-to-end.**

---

## 🧠 Why ImpByte Is Multimodal

ImpByte fuses **multiple complementary signals**:

### 🔊 Audio Intelligence (How it’s said)

* Detects loudness and emphasis peaks
* Captures excitement, stress, and importance

### 🧠 Speech Understanding (What is said)

* Uses **OpenAI Whisper**
* Produces timestamped transcript segments
* Filters filler and incomplete speech

### 🤖 Semantic Reasoning (Why it matters)

* Uses **Google Gemini 2.5 Flash**
* Ranks candidate segments by reel-worthiness
* Selects standalone, meaningful ideas

👉 Only moments that are **energetic AND meaningful** are selected.

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

ImpByte intelligently adapts to **any input video shape**:

| Input Type        | Example                | Output Behavior                |
| ----------------- | ---------------------- | ------------------------------ |
| Vertical (9:16)   | Phone-recorded video   | Preserved as-is                |
| Horizontal (16:9) | YouTube / laptop video | Scaled + padded to 9:16        |
| Square / 4:3      | Mixed sources          | Scaled + padded                |
| Any               |                        | ❌ No cropping, ❌ no distortion |

This guarantees **zero content loss** while maintaining a **native mobile viewing experience**.

---

## ✨ Key Features

* Automatic highlight detection
* Multimodal reasoning (audio + language)
* Semantic ranking using Gemini 2.5 Flash
* Dynamic clip lengths (40–100 seconds)
* Aspect-aware vertical reel conversion
* No cropping of original content
* High-contrast caption burn-in
* Deterministic FFmpeg-based pipeline
* CLI pipeline + Streamlit UI
* Robust fallbacks for stability

---

## 🎥 Demo – Input & Generated Outputs

ImpByte was evaluated end-to-end on a real long-form video.

### ▶️ Input: Long-Form Video

Original source video provided to the system:

🔗 [https://drive.google.com/file/d/1KDf3N9E1lU5IBJpyhOvVsc2HCjg8G5mr/view](https://drive.google.com/file/d/1KDf3N9E1lU5IBJpyhOvVsc2HCjg8G5mr/view)

---

### 📱 Output: Generated Reels (9:16)

All reels automatically generated from the above input video:

📂 [https://drive.google.com/drive/folders/1pcglVT7XghZ9eUsYN2gRiMWo_OjgK3ue](https://drive.google.com/drive/folders/1pcglVT7XghZ9eUsYN2gRiMWo_OjgK3ue)

---

### What this demo demonstrates:

* Automatic detection of multiple high-impact moments
* Semantic segment selection (not random cuts)
* Dynamic clip durations
* Aspect-aware 9:16 formatting
* No cropping of original content
* Caption burn-in optimized for mobile viewing

All outputs were generated **fully automatically**, with:

* No manual timestamp selection
* No manual cropping
* No manual captioning

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

### 1️⃣ Setup

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

```text
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

## 🖥️ Streamlit Demo UI

```bash
streamlit run app.py
```

### UI Features

* Upload long-form video
* Automatic processing
* Preview generated reels
* Same backend as CLI (no divergence)

---

## 🧠 Engineering Highlights

* Aspect-aware video processing
* Deterministic FFmpeg pipeline (no ImageMagick)
* Defensive GenAI integration with safe fallbacks
* Clear separation of perception, reasoning, and execution
* Designed for real-world creator workflows

---

## 🚧 Limitations & Future Work

* Face-aware smart cropping (MediaPipe)
* Word-level karaoke captions
* Blurred or branded background padding
* Auto-generated hook text
* GPU acceleration for faster processing

---

## 🏁 Conclusion

ImpByte demonstrates how **multimodal AI** can be combined with **practical video engineering** to solve real creator problems.

It transforms a single long-form video into **multiple high-quality, platform-ready reels**, reducing manual effort while preserving content integrity.

---

## 👤 Author

**Ashant Kumar**

