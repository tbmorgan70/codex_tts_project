# Codex Local TTS Project Starter

This starter is designed for a **persistent Codex project** on **Windows + NVIDIA GPU** with a clean Python environment.

## Recommended default stack

**Primary recommendation:** XTTS v2 via `coqui-tts`

Why:
- best balance of quality, voice cloning, multilingual support, and project maturity
- works from a short reference WAV
- can be run fully local
- easier "single project folder" workflow than F5-TTS

## Fallback options

### Kokoro
Use this when you want:
- very light local TTS
- fast setup
- built-in voices / blending
- less dependency drama

### F5-TTS
Use this when you want:
- frontier-quality zero-shot style work
- willingness to deal with more moving parts
- reference audio + transcript workflows

## Important environment rule

Pin Python on purpose.

For this project, use:

- **Python 3.11.x**
- fresh virtual environment
- PyTorch installed first, matching your CUDA wheel

Do **not** let the environment drift to 3.13+ unless you intentionally rebuild around newer support.

---

## Project layout

- `requirements_xtts.txt` — default install path
- `requirements_kokoro.txt` — lightweight fallback
- `run_xtts.py` — generate speech from a voice sample
- `check_gpu.py` — verify torch/CUDA
- `settings.example.json` — editable config
- `voices/` — put your source WAV files here
- `input/` — text inputs
- `output/` — generated audio
- `notes/` — transcripts and reference notes

---

## What to put in `voices/`

Create a clean WAV like:

`voices/tim_reference.wav`

Recommended source clip:
- mono or stereo is fine
- 16-bit PCM WAV is safest
- 22050 Hz to 48000 Hz is usually fine
- 6–20 seconds of clean speech
- minimal room noise
- no music bed
- no heavy compression/reverb
- avoid shouting and whispering

Also save a transcript for reference quality control:

`notes/tim_reference_transcript.txt`

---

## Install sequence in Codex terminal

### 1) Create venv
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
```

### 2) Install PyTorch first
Pick the command from the official PyTorch install page for your CUDA setup.
Example for CUDA 11.8 wheels:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3) Install XTTS stack
```bash
pip install -r requirements_xtts.txt
```

This project currently pins `transformers` to a compatible 4.x release in
`requirements_xtts.txt`. Keep that pin unless you intentionally re-test XTTS
with a newer `coqui-tts` stack.

### 4) Verify GPU
```bash
python check_gpu.py
```

### 5) Edit config
Copy:
```bash
copy settings.example.json settings.json
```

Then update the paths and text.

### 6) Generate a test WAV
```bash
python run_xtts.py
```

On first XTTS run, Coqui will require acceptance of the XTTS model terms
before downloading model files. For non-interactive runs, set:

```bash
set COQUI_TOS_AGREED=1
python run_xtts.py
```

If you are using PowerShell:

```powershell
$env:COQUI_TOS_AGREED="1"
python run_xtts.py
```

---

## Working Notes For This Machine

- Use standard CPython 3.11, not the Inkscape-bundled Python.
- The working environment here used `Python 3.11.9`.
- GPU verification passed with `torch 2.7.1+cu118` on an NVIDIA RTX 4060.
- `coqui-tts 0.27.5` currently has a runtime mismatch with the newest
  `transformers` API for XTTS. This project works by:
  - pinning `transformers` in `requirements_xtts.txt`
  - applying a small local compatibility shim in `run_xtts.py`
- Keep those two fixes in place unless you intentionally retest and remove them.

---

## Notes for Codex

In Codex, tell it:

- keep this folder structure intact
- do not upgrade Python without checking TTS compatibility
- do not replace `coqui-tts` with legacy `TTS` package unless explicitly requested
- install torch first
- keep generated files inside `output/`
- keep reference WAVs inside `voices/`
- save all setup changes into this folder only

---

## When to switch models

Stay with **XTTS** if:
- you want voice cloning from a short WAV
- you want decent quality without a huge training pipeline
- you want the most practical balance

Switch to **Kokoro** if:
- XTTS installation gets weird
- you mainly want fast local voices, not deep cloning/training
- you want a lighter secondary engine

Switch to **F5-TTS** if:
- you want to experiment with best-in-class zero-shot behavior
- you’re okay with more dependency work
- non-commercial pretrained model licensing is acceptable for your use case
