import os
import subprocess
from moviepy import VideoFileClip

from utils.transcript_utils import find_dynamic_end


# -------------------------------------------------
# Vertical reel conversion (Guaranteed 9:16)
# -------------------------------------------------
def convert_to_vertical_ffmpeg(input_path: str, output_path: str):
    """
    Convert video into 9:16 reel format intelligently:

    - If video is already vertical (phone-recorded), keep as-is
    - If video is horizontal, fit inside 9:16 with padding
    - Never crop original content
    """

    # Step 1: Probe resolution
    probe_cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        input_path
    ]

    result = subprocess.check_output(probe_cmd).decode().strip()
    width, height = map(int, result.split(","))

    # Step 2: Decide behavior
    if height >= width:
        # Already vertical (phone video)
        print("📱 Input is vertical — keeping original framing")

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            output_path
        ]

    else:
        # Horizontal video → fit + pad
        print("💻 Input is horizontal — fitting into 9:16 with padding")

        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf",
            (
                "scale=1080:-1,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black"
            ),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            output_path
        ]

    subprocess.run(cmd, check=True)



# -------------------------------------------------
# Caption burn-in (Reliable, FFmpeg-based)
# -------------------------------------------------
def burn_caption_ffmpeg(input_path: str, output_path: str, caption_text: str):
    """
    Burn a high-contrast, reel-safe caption onto the video.
    """

    safe_text = (
        caption_text.replace(":", "")
        .replace("'", "")
        .replace('"', "")
        .replace("\n", " ")
    )

    drawtext = (
        "drawtext="
        f"text='{safe_text}':"
        "fontcolor=white:"
        "fontsize=52:"
        "box=1:"
        "boxcolor=black@0.65:"
        "boxborderw=14:"
        "x=(w-text_w)/2:"
        "y=h-300"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", drawtext,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        output_path
    ]

    subprocess.run(cmd, check=True)


# -------------------------------------------------
# Main reel generation pipeline (Dynamic 40–100s)
# -------------------------------------------------
def generate_reels(
    video_path,
    segments,
    transcript_segments,
    output_dir="output/clips"
):
    """
    FINAL Reel Pipeline:
    - Semantic start (from Gemini-ranked segments)
    - Dynamic semantic end (40–100s)
    - FFmpeg vertical conversion
    - FFmpeg caption burn-in
    """

    os.makedirs(output_dir, exist_ok=True)

    video = VideoFileClip(video_path)
    results = []

    for idx, seg in enumerate(segments, 1):
        # -------------------------------------------------
        # Dynamic semantic start & end
        # -------------------------------------------------
        start_time = seg["start"]

        end_time = find_dynamic_end(
            start_time=start_time,
            segments=transcript_segments,
            min_len=40,
            max_len=100
        )

        # Safety fallback
        if end_time is None:
            end_time = start_time + 60

        # Clamp to video duration
        end_time = min(end_time, video.duration)

        # Debug (IMPORTANT)
        print(
            f"🎯 Reel {idx}: "
            f"start={start_time:.2f}s | "
            f"end={end_time:.2f}s | "
            f"dur={end_time - start_time:.2f}s"
        )

        # -------------------------------------------------
        # Output paths
        # -------------------------------------------------
        horizontal_path = os.path.join(
            output_dir, f"reel_{idx}.mp4"
        )
        vertical_path = os.path.join(
            output_dir, f"reel_{idx}_vertical.mp4"
        )
        captioned_path = os.path.join(
            output_dir, f"reel_{idx}_vertical_captioned.mp4"
        )

        # -------------------------------------------------
        # Horizontal clip extraction
        # -------------------------------------------------
        clip = video.subclipped(start_time, end_time)
        clip.write_videofile(
            horizontal_path,
            codec="libx264",
            audio_codec="aac"
        )
        clip.close()

        # -------------------------------------------------
        # Vertical reel
        # -------------------------------------------------
        convert_to_vertical_ffmpeg(
            horizontal_path,
            vertical_path
        )

        # -------------------------------------------------
        # Caption burn-in
        # -------------------------------------------------
        burn_caption_ffmpeg(
            vertical_path,
            captioned_path,
            seg["text"]
        )

        results.append({
            "horizontal": horizontal_path,
            "vertical": vertical_path,
            "captioned": captioned_path
        })

    video.close()
    return results
