# codex_tts_project

## Features

- Local XTTS voice cloning on Windows
- Dedicated Python 3.11 virtual environment
- PyTorch with CUDA GPU support
- Reference WAV based voice generation
- Persistent project structure for Codex workflows
- Documented compatibility fixes for repeatable setup

## Project Goal

Set up a stable, local text-to-speech workflow using **Coqui XTTS** so the project could generate speech from a reference voice sample without relying on a hosted API.

## What Was Done

### 1. Fixed the Python environment

The first blocker was that the system `python` command pointed to **Inkscape’s bundled Python**, which was not compatible with standard PyTorch wheels. A proper **CPython 3.11** installation was added, and the project was rebuilt around that interpreter.

### 2. Created a clean project environment

A fresh virtual environment was created inside the repo using:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
```

This ensured the project used a controlled Python environment instead of whatever Windows happened to find first.

### 3. Installed core dependencies

The setup included:

- upgraded `pip`, `setuptools`, and `wheel`
- installed **PyTorch 2.7.1 + cu118**
- installed **torchvision** and **torchaudio**
- installed XTTS dependencies from `requirements_xtts.txt`
- installed **coqui-tts 0.27.5**

### 4. Verified runtime support

The environment was checked to confirm:

- Python 3.11.9 was active inside the virtual environment
- the required packages installed correctly
- GPU support worked on the **RTX 4060**
- project paths for input and output files were correct

### 5. Completed the XTTS workflow

After adding the reference voice WAV file, the XTTS workflow was tested end to end. A compatibility issue in the local XTTS setup was fixed by updating:

- `run_xtts.py`
- `requirements_xtts.txt`
- `settings.json`

The XTTS model was then downloaded and used to generate:

- `tim_test_xtts.wav`

## Result

The repository now contains a working local XTTS setup with:

- a functioning `.venv`
- compatible Python and package versions
- GPU-enabled inference
- a reference voice cloning workflow
- a successful generated test output

## Stack

- Windows PowerShell
- Python 3.11.9
- PyTorch 2.7.1 + cu118
- Coqui XTTS / `coqui-tts`
- NVIDIA RTX 4060

## Usage Notes

This repo is intended as a reusable local TTS project. The setup process showed that interpreter selection matters as much as package installation, especially for machine learning tools on Windows. Once the correct Python environment was in place, the rest of the stack could be installed and tested successfully.

## Outcome

This project produced a working, repeatable XTTS voice cloning environment that can now be used for additional testing, prompt variation, batch generation, or future voice-based workflows.
