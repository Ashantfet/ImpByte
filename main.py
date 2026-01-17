from moviepy import VideoFileClip

from utils.audio_utils import extract_loudness_peaks
from utils.transcript_utils import (
    transcribe_video,
    get_relevant_segments
)
from utils.gemini_utils import rank_segments_with_gemini
from utils.video_utils import generate_reels


# -------------------------------------------------
# Configuration
# -------------------------------------------------
VIDEO_PATH = "input/test_video.mp4"
OUTPUT_DIR = "output/clips"

TOP_K_PEAKS = 5
MIN_WORDS = 6
PEAK_WINDOW = 15          # seconds


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------
def main():
    print("\n================ ByteSize Pipeline ================\n")

    # -------------------------------------------------
    # 1. Video Sanity Check
    # -------------------------------------------------
    print("🔍 Loading input video...")
    video = VideoFileClip(VIDEO_PATH)
    print("✅ Video loaded")
    print(f"   Duration   : {video.duration:.2f}s")
    print(f"   Resolution : {video.size}")
    video.close()

    # -------------------------------------------------
    # 2. Audio Loudness Peaks
    # -------------------------------------------------
    print("\n🔊 Extracting loudness peaks...")
    peaks = extract_loudness_peaks(
        VIDEO_PATH,
        top_k=TOP_K_PEAKS
    )

    if not peaks:
        print("⚠️ No audio peaks detected. Exiting.")
        return

    print("🔥 Loudness peaks detected at:")
    for t in peaks:
        print(f"   - {t:.2f}s")

    # -------------------------------------------------
    # 3. Transcription (Whisper)
    # -------------------------------------------------
    print("\n🧠 Transcribing video with OpenAI Whisper...")
    segments = transcribe_video(
        VIDEO_PATH,
        model_size="base"
    )

    if not segments:
        print("⚠️ Transcription failed or empty. Exiting.")
        return

    print(f"✅ Transcription complete ({len(segments)} segments)")

    # -------------------------------------------------
    # 4. Heuristic Multimodal Fusion
    # -------------------------------------------------
    print("\n🔗 Selecting candidate highlight segments...")
    candidate_segments = get_relevant_segments(
        segments=segments,
        peaks=peaks,
        window=PEAK_WINDOW,
        min_words=MIN_WORDS
    )

    if not candidate_segments:
        print("⚠️ No high-value segments found. Exiting.")
        return

    print(f"✨ {len(candidate_segments)} candidate segments identified")

    # -------------------------------------------------
    # 5. Semantic Refinement (Gemini 2.5 Flash)
    # -------------------------------------------------
    print("\n🤖 Refining highlights with Gemini 2.5 Flash...")
    refined_segments = rank_segments_with_gemini(
        candidate_segments,
        top_k=5
    )

    if not refined_segments:
        print("⚠️ Gemini returned no usable segments. Exiting.")
        return

    print("\n🏆 Final selected segments:")
    for i, seg in enumerate(refined_segments, 1):
        print(
            f"{i}. [{seg['start']:.2f}s - {seg['end']:.2f}s] "
            f"{seg['text'][:80]}..."
        )
        if "reason" in seg:
            print(f"   ↳ Reason: {seg['reason']}")

    # -------------------------------------------------
    # 6. Reel Generation (Dynamic 40–100s)
    # -------------------------------------------------
    print("\n🎬 Generating reels (Dynamic 40–100s)...")

    reels = generate_reels(
        video_path=VIDEO_PATH,
        segments=refined_segments,
        transcript_segments=segments,   # FULL Whisper transcript
        output_dir=OUTPUT_DIR
    )

    if not reels:
        print("⚠️ Reel generation failed.")
        return

    print("\n✅ Reels generated successfully:")
    for r in reels:
        print("   Horizontal :", r["horizontal"])
        print("   Vertical   :", r["vertical"])
        print("   Captioned  :", r["captioned"])
        print()

    print("=============== Pipeline Complete ===============\n")


# -------------------------------------------------
# Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    main()
