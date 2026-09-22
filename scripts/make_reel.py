#!/usr/bin/env python3
"""Convert a 1080x1350 card news image into a vertical Instagram Reels video
with the fixed '헤드라인' background music track.

Usage:
    python scripts/make_reel.py --photo assets/daily/2026-09-23/card_1.png \
        --out assets/daily/2026-09-23/reel_1.mp4 [--duration 12]
"""
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BGM_PATH = REPO_ROOT / "assets" / "bgm" / "headline.mp3"

# Reels canvas: 1080x1920 (9:16). Card is 1080x1350, so we pad top/bottom
# with a blurred, darkened copy of the same image for a clean full-bleed look.
CANVAS_W, CANVAS_H = 1080, 1920


def build_filter(duration: float) -> str:
    return (
        f"[0:v]scale=-1:{CANVAS_H},crop={CANVAS_W}:{CANVAS_H},boxblur=40:20,eq=brightness=-0.08[bg];"
        f"[0:v]scale={CANVAS_W}:-1[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2[v];"
        f"[v]fade=t=in:st=0:d=0.4,fade=t=out:st={duration - 0.5}:d=0.5[vout]"
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--photo", required=True, help="Path to the 1080x1350 card PNG")
    p.add_argument("--out", required=True, help="Output MP4 path")
    p.add_argument("--duration", type=float, default=12.0, help="Reel length in seconds (default 12)")
    p.add_argument("--bgm", default=str(BGM_PATH), help="Background music file (defaults to fixed headline track)")
    p.add_argument("--bgm-start", type=float, default=0.0, help="Seconds into the BGM file to start from")
    args = p.parse_args()

    photo = Path(args.photo)
    out = Path(args.out)
    bgm = Path(args.bgm)

    if not photo.exists():
        print(f"ERROR: photo not found: {photo}", file=sys.stderr)
        return 1
    if not bgm.exists():
        print(f"ERROR: bgm not found: {bgm}", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(photo),
        "-ss", str(args.bgm_start), "-t", str(args.duration), "-i", str(bgm),
        "-filter_complex", build_filter(args.duration),
        "-map", "[vout]", "-map", "1:a",
        "-t", str(args.duration),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(out),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-3000:], file=sys.stderr)
        return result.returncode

    print(f"saved {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
