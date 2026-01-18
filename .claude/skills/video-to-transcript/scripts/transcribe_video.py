#!/usr/bin/env python3
"""
Video to Transcript Converter

Converts video files to timestamped markdown transcripts using ffmpeg and OpenAI Whisper.
Supports multiple languages and common video formats.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    # Check ffmpeg
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "ffmpeg is not installed. Please install ffmpeg first."

    # Check whisper
    try:
        import whisper
        return True, None
    except ImportError:
        return False, "openai-whisper is not installed. Run: pip install openai-whisper"


def extract_audio(video_path: str, audio_path: str) -> bool:
    """Extract audio from video using ffmpeg."""
    print(f"🎬 Extracting audio from: {video_path}")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM 16-bit little-endian
        "-ar", "16000",  # Sample rate 16kHz (optimal for Whisper)
        "-ac", "1",  # Mono
        "-y",  # Overwrite output file
        audio_path
    ]

    try:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True
        )
        print(f"✅ Audio extracted to: {audio_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error extracting audio: {e.stderr.decode()}")
        return False


def transcribe_audio(
    audio_path: str,
    model_size: str = "medium",
    language: str = None
) -> dict:
    """Transcribe audio using OpenAI Whisper."""
    import whisper

    print(f"🎙️  Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    print(f"📝 Transcribing audio...")
    options = {
        "task": "transcribe",
        "verbose": False
    }

    if language:
        options["language"] = language

    result = model.transcribe(audio_path, **options)
    print("✅ Transcription complete")

    return result


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    return str(timedelta(seconds=int(seconds)))


def create_markdown(
    result: dict,
    video_path: str,
    output_path: str,
    include_timestamps: bool = True,
    group_by_paragraph: bool = True
):
    """Create markdown transcript from Whisper result."""

    video_name = Path(video_path).stem
    segments = result.get("segments", [])
    text = result.get("text", "")

    lines = []
    lines.append(f"# Transcript: {video_name}\n")
    lines.append(f"**Source:** `{video_path}`\n")
    lines.append(f"**Language:** {result.get('language', 'auto-detected')}\n")

    if result.get("duration"):
        duration = format_timestamp(result["duration"])
        lines.append(f"**Duration:** {duration}\n")

    lines.append("\n---\n\n")

    # Full text section
    lines.append("## Full Text\n\n")
    lines.append(text.strip() + "\n\n")

    # Timestamped segments
    if include_timestamps and segments:
        lines.append("## Timestamped Segments\n\n")

        if group_by_paragraph:
            # Group segments into paragraphs (combine short segments)
            current_para = []
            para_start = None

            for i, seg in enumerate(segments):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])

                if not current_para:
                    para_start = start
                    current_para.append(seg["text"].strip())
                elif len(seg["text"].strip()) < 50 and seg["text"].strip()[0] not in ".!?。!?":
                    # Continue paragraph
                    current_para.append(seg["text"].strip())
                else:
                    # End paragraph and start new one
                    para_text = " ".join(current_para)
                    lines.append(f"**[{para_start}]** {para_text}\n\n")
                    current_para = [seg["text"].strip()]
                    para_start = start

            # Add last paragraph
            if current_para:
                para_text = " ".join(current_para)
                lines.append(f"**[{para_start}]** {para_text}\n\n")
        else:
            # Individual segments
            for seg in segments:
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                lines.append(f"**[{start} - {end}]** {seg['text'].strip()}\n\n")

    # Write to file
    output_content = "".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)

    print(f"✅ Markdown transcript saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert video to markdown transcript using Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  %(prog)s video.mp4

  # Specify output file
  %(prog)s video.mp4 -o transcript.md

  # Use larger model for better accuracy
  %(prog)s video.mp4 --model large

  # Specify language
  %(prog)s video.mp4 --language zh

  # Combine options
  %(prog)s video.mp4 -o output.md --model medium --language en
        """
    )

    parser.add_argument(
        "video",
        help="Path to video file"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output markdown file path (default: video_name.md)",
        default=None
    )

    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        default="medium",
        help="Whisper model size (default: medium)"
    )

    parser.add_argument(
        "--language",
        help="Language code (e.g., en, zh, ja, es). Auto-detect if not specified."
    )

    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        help="Don't include timestamps in output"
    )

    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep extracted audio file"
    )

    parser.add_argument(
        "--audio-only",
        type=str,
        metavar="AUDIO_PATH",
        help="Use existing audio file instead of extracting from video"
    )

    args = parser.parse_args()

    # Check dependencies
    ok, msg = check_dependencies()
    if not ok:
        print(f"❌ {msg}", file=sys.stderr)
        print("\nInstallation instructions:", file=sys.stderr)
        print("  ffmpeg: https://ffmpeg.org/download.html", file=sys.stderr)
        print("  whisper: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    # Determine paths
    video_path = Path(args.video).resolve()
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = video_path.parent / f"{video_path.stem}.md"

    # Use existing audio or extract from video
    if args.audio_only:
        audio_path = Path(args.audio_only).resolve()
        if not audio_path.exists():
            print(f"❌ Audio file not found: {audio_path}", file=sys.stderr)
            sys.exit(1)
        print(f"🎵 Using existing audio: {audio_path}")
    else:
        audio_path = video_path.parent / f"{video_path.stem}_audio.wav"
        if not extract_audio(str(video_path), str(audio_path)):
            sys.exit(1)

    # Transcribe
    try:
        result = transcribe_audio(
            str(audio_path),
            model_size=args.model,
            language=args.language
        )
    except Exception as e:
        print(f"❌ Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Create markdown
    create_markdown(
        result,
        str(video_path),
        str(output_path),
        include_timestamps=not args.no_timestamps
    )

    # Cleanup
    if not args.keep_audio and not args.audio_only and audio_path.exists():
        audio_path.unlink()
        print(f"🧹 Removed temporary audio file")

    print(f"\n✨ Done! Transcript saved to: {output_path}")


if __name__ == "__main__":
    main()
