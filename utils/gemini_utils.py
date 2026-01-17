import os
import json
from google import genai


# =================================================
# Gemini Configuration
# =================================================

if "GOOGLE_API_KEY" not in os.environ:
    raise EnvironmentError(
        "GOOGLE_API_KEY not found. "
        "Export it using: export GOOGLE_API_KEY=your_key"
    )

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# VERIFIED AVAILABLE MODEL (from models.list())
MODEL_NAME = "models/gemini-2.5-flash"


# =================================================
# Gemini-based semantic ranking
# =================================================
def rank_segments_with_gemini(segments, top_k=5):
    """
    Uses Gemini 2.5 Flash to semantically rank transcript segments.

    Input:
        segments: list of {
            "start": float,
            "end": float,
            "text": str
        }

    Output:
        list of {
            "start": float,
            "end": float,
            "text": str,
            "reason": str
        }

    Safety:
        - Forces JSON-only output
        - Guards against malformed responses
        - Falls back to heuristic segments
    """

    if not segments:
        return []

    # Build transcript block
    transcript = "\n".join(
        f"[{s['start']:.2f} - {s['end']:.2f}] {s['text']}"
        for s in segments
    )

    # STRONG JSON-ONLY PROMPT
    prompt = f"""
You are a JSON API.

Your task is to select the TOP {top_k} transcript segments
that are best suited for a 40–100 second social media reel.

STRICT RULES:
- Respond with RAW JSON ONLY
- Do NOT include markdown
- Do NOT include explanations
- Do NOT include backticks
- Do NOT include extra text
- Output must be valid JSON

JSON FORMAT (must match exactly):
[
  {{
    "start": <float>,
    "end": <float>,
    "reason": "<string>"
  }}
]

Transcript:
{transcript}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw = response.text.strip()

        # -------------------------------
        # Hard guards against bad output
        # -------------------------------
        if not raw:
            raise ValueError("Empty Gemini response")

        if not raw.startswith("["):
            raise ValueError("Non-JSON Gemini response")

        ranked = json.loads(raw)

        if not isinstance(ranked, list):
            raise ValueError("Gemini JSON is not a list")

        # Map Gemini output back to original segments
        final_segments = []

        for r in ranked:
            if "start" not in r or "end" not in r:
                continue

            for s in segments:
                if abs(s["start"] - float(r["start"])) < 0.5:
                    final_segments.append({
                        "start": s["start"],
                        "end": s["end"],
                        "text": s["text"],
                        "reason": r.get("reason", "")
                    })
                    break

        # Final clamp
        return final_segments[:top_k]

    except Exception as e:
        print("⚠️ Gemini failed, falling back to heuristic segments.")
        print("   Reason:", e)
        return segments[:top_k]
