---
name: video-to-transcript
description: "Convert local video files (mp4, mov, avi, mkv, etc.) to timestamped markdown transcripts using OpenAI Whisper. Use when a user asks to transcribe a video, convert video to text, create subtitles from video, extract speech from video, or generate meeting/interview/conversation transcripts from video files."
---

# Video to Transcript

Convert local video files to formatted markdown transcripts with timestamps.

## Quick Start

```bash
# Basic usage
python scripts/transcribe_video.py path/to/video.mp4

# Specify output file
python scripts/transcribe_video.py video.mp4 -o transcript.md

# Use larger model for better accuracy (slower)
python scripts/transcribe_video.py video.mp4 --model large

# Specify language (zh, en, ja, es, etc.)
python scripts/transcribe_video.py video.mp4 --language zh
```

## Sandbox Environment

This skill is sandbox-compatible and automatically uses `TMPDIR` environment variable for temporary files (default: `/tmp/claude`).

**When running in sandbox:**
1. Ensure ffmpeg is accessible (may need to disable sandbox temporarily)
2. Output files must be in allowed directories (current directory, Downloads, etc.)
3. Temporary audio files are stored in `TMPDIR` and auto-cleaned

**To disable sandbox if needed:**
```bash
/sandbox
```

Then re-enable after transcription completes.

## Prerequisites

### 1. Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### 2. Install OpenAI Whisper

```bash
pip install openai-whisper
```

**Optional:** Install faster-whisper for improved speed:
```bash
pip install faster-whisper
```

## Usage Patterns

### Common User Requests

**"Transcribe this interview video"**
```bash
python scripts/transcribe_video.py interview.mp4 -o interview_transcript.md
```

**"Convert this video to text with timestamps"**
```bash
python scripts/transcribe_video.py meeting.mp4 --model medium
```

**"Extract Chinese audio from this video"**
```bash
python scripts/transcribe_video.py video.mp4 --language zh
```

### Command Options

| Option | Description |
|--------|-------------|
| `video` | Path to video file (required) |
| `-o, --output` | Output markdown file path |
| `--model` | Model size: tiny, base, small, medium (default), large, large-v2, large-v3 |
| `--language` | Language code (en, zh, ja, es, fr, de, etc.) |
| `--no-timestamps` | Omit timestamps from output |
| `--keep-audio` | Keep extracted audio file |
| `--audio-only` | Use existing audio file instead of extracting |
| `--temp-dir` | Custom temp directory (default: TMPDIR or /tmp/claude) |

## Model Selection

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~39MB | Fastest | Lowest |
| base | ~74MB | Fast | Basic |
| small | ~244MB | Moderate | Good |
| **medium** | ~769MB | **Balanced** | **Recommended** |
| large-v3 | ~1550MB | Slowest | Best |

**Recommendation:** Start with `medium` model. Use `large-v3` for critical content or multiple speakers.

## Output Format

Generated markdown includes:

1. **Full Text** - Complete transcript without timestamps
2. **Timestamped Segments** - Segments grouped by paragraph with timestamps in `[HH:MM:SS]` format

Example output:
```markdown
# Transcript: interview_2024

**Source:** `interview_2024.mp4`
**Language:** zh
**Duration:** 0:45:30

---

## Full Text

[Complete text content...]

## Timestamped Segments

**[00:00:15]** 首先感谢您接受我们的采访...
**[00:02:30]** 关于这个项目，我认为...
```

## Supported Video Formats

- MP4 (`.mp4`)
- QuickTime (`.mov`, `.qt`)
- AVI (`.avi`)
- MKV (`.mkv`)
- WebM (`.webm`)
- Most formats supported by ffmpeg

## Supported Languages

Auto-detection supports 99 languages. Common codes:

- `zh` - Chinese
- `en` - English
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- `de` - German
- `ru` - Russian

See Whisper documentation for complete list.

## Script

The main script `scripts/transcribe_video.py` handles:

1. Extract audio from video using ffmpeg
2. Transcribe audio with OpenAI Whisper
3. Generate formatted markdown with timestamps
4. Clean up temporary files

Run with `--help` for complete usage information.
