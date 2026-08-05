# Codex TTS Project

Local, GPU-assisted voice cloning with Coqui XTTS on Windows.

**Current workflow version: v0.2.1**

## What v0.2.1 adds

- Automatic, non-destructive reference preparation by default.
- Prepared reference audio is refreshed only when its raw source changes.

## What v0.2.0 adds

- Text-file input through `text_file`.
- Speech-rate control through `speed`.
- Repeatable generation through an optional `seed`.
- `focused`, `natural`, and `expressive` delivery presets.
- Single-file or multi-reference voice input: set `speaker_wav` to an audio file or a folder of reference clips.

See [Voice Workflow](docs/VOICE_WORKFLOW.md) for reference preparation and generation guidance, and [CHANGELOG.md](CHANGELOG.md) for version history.

## Quick Start

Run commands from `codex_tts_project/codex_tts_project`.

```powershell
Copy-Item settings.example.json settings.json
$env:COQUI_TOS_AGREED = "1"
.\.venv\Scripts\python.exe run_xtts.py
```

Edit `settings.json` to select the text, voice reference, delivery preset, and output filename.

## Example Configuration

```json
{
  "text_file": "input/my_script.txt",
  "language": "en",
  "speed": 1.0,
  "preset": "natural",
  "seed": 42,
  "prepare_references": true,
  "speaker_wav": "voices/my_voice",
  "output_wav": "output/my_voice_take.wav"
}
```

When `speaker_wav` points to a folder, the runner uses supported files in filename order: WAV, MP3, FLAC, M4A, and OGG.

## Requirements

- Windows
- Python 3.11
- NVIDIA GPU recommended
- Coqui XTTS dependencies from `requirements_xtts.txt`

Use [README_SETUP.md](codex_tts_project/codex_tts_project/README_SETUP.md) for full environment setup.