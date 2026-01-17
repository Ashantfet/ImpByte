import streamlit as st
import os
import tempfile

from utils.audio_utils import extract_loudness_peaks
from utils.transcript_utils import (
    transcribe_video,
    get_relevant_segments
)
from utils.gemini_utils import rank_segments_with_gemini
from utils.video_utils import generate_reels


# -------------------------------------------------
# Streamlit page config
# -------------------------------------------------
st.set_page_config(
    page_title="ByteSize – Automatic Reel Generator",
    layout="centered"
)

st.title("🎬 ByteSize – Automatic Reel Generator")
st.markdown(
    """
    Upload a **long-form video** (lecture, interview, podcast) and automatically
    generate **high-impact short reels** using **multimodal AI**:

    - 🔊 Audio loudness (emotion / emphasis)
    - 🧠 Speech understanding (Whisper)
    - 🤖 Semantic reasoning (Gemini)
    - 🎥 Automatic reel generation
    - 📱 Reels/TikTok-ready vertical videos
    - 📝 Timed captions
    """
)

# -------------------------------------------------
# Video upload
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a video file",
    type=["mp4", "mov", "mkv"]
)

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, uploaded_file.name)

        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("✅ Video uploaded successfully!")

        if st.button("🚀 Generate Reels"):
            with st.spinner("Processing video (this may take a few minutes)..."):

                # -------------------------------------------------
                # Phase 1: Audio loudness
                # -------------------------------------------------
                st.write("🔊 Detecting loudness peaks...")
                peaks = extract_loudness_peaks(video_path, top_k=5)

                if not peaks:
                    st.warning("⚠️ No loudness peaks detected.")
                    st.stop()

                # -------------------------------------------------
                # Phase 2: Transcription
                # -------------------------------------------------
                st.write("🧠 Transcribing video with Whisper...")
                segments = transcribe_video(video_path, model_size="base")

                if not segments:
                    st.warning("⚠️ Transcription failed.")
                    st.stop()

                # -------------------------------------------------
                # Phase 3: Heuristic multimodal fusion
                # -------------------------------------------------
                st.write("🔗 Matching loudness with meaningful speech...")
                candidate_segments = get_relevant_segments(
                    segments=segments,
                    peaks=peaks,
                    window=15,
                    min_words=6
                )

                if not candidate_segments:
                    st.warning("⚠️ No high-value moments detected.")
                    st.stop()

                # -------------------------------------------------
                # Phase 4: Gemini semantic refinement
                # -------------------------------------------------
                st.write("🤖 Refining highlights with Gemini 2.5 Flash...")
                refined_segments = rank_segments_with_gemini(
                    candidate_segments,
                    top_k=5
                )

                if not refined_segments:
                    st.warning("⚠️ Gemini returned no usable segments.")
                    st.stop()

                # -------------------------------------------------
                # Phase 5: Reel generation (Dynamic 40–100s)
                # -------------------------------------------------
                st.write("🎬 Generating reels (dynamic 40–100s)...")
                reels = generate_reels(
                    video_path=video_path,
                    segments=refined_segments,
                    transcript_segments=segments,
                    output_dir="output/clips"
                )

                if not reels:
                    st.warning("⚠️ Reel generation failed.")
                    st.stop()

                st.success("🎉 Reels generated successfully!")

                # -------------------------------------------------
                # Display results
                # -------------------------------------------------
                st.subheader("📂 Generated Reels")

                for i, reel in enumerate(reels, 1):
                    st.markdown(f"## Reel {i}")

                    st.markdown("### 🎥 Horizontal (16:9)")
                    st.video(reel["horizontal"])

                    st.markdown("### 📱 Vertical (9:16)")
                    st.video(reel["vertical"])

                    st.markdown("### 📝 Vertical with Captions")
                    st.video(reel["captioned"])
                    st.markdown("---")