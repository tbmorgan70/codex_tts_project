# codex_tts_project

## Project Overview

This repository documents the setup of a local **XTTS voice cloning** environment on Windows for use inside a persistent Codex project. The goal was to create a stable, repeatable setup that could run locally with GPU support, use a reference voice sample, and generate speech output without relying on a hosted API.

## Objective

The objective was to configure the repository so it could:

- run on a dedicated Python virtual environment
- use a compatible local Python installation
- install PyTorch with CUDA support
- run Coqui XTTS with a reference WAV file
- generate a local voice clone test output

## Environment

The project was set up in a Windows PowerShell environment inside the repository folder:

`C:\Users\tbmor\Desktop\code\codex_tts_project\codex_tts_project`

A fresh virtual environment was created with:

- **Python 3.11.9**
- `.venv` inside the project directory

The virtual environment activated successfully and the project used Python 3.11.9 as intended.

## Initial Problem

The first major issue was that the default `python` command on the system was resolving to **Inkscape’s bundled Python** rather than a standard Windows CPython installation. That interpreter used incompatible wheel tags, which prevented installation of normal machine learning packages such as PyTorch.

The solution was to install **standard CPython 3.11.x** and rebuild the virtual environment from that interpreter.

## Setup Process

After the correct Python version was installed, the following steps were completed:

1. A new `.venv` was created in the project folder using `py -3.11 -m venv .venv`
2. The environment was activated successfully
3. `pip`, `setuptools`, and `wheel` were upgraded
4. **PyTorch 2.7.1+cu118**, `torchvision`, and `torchaudio` were installed
5. The project requirements in `requirements_xtts.txt` were installed, including **coqui-tts 0.27.5** and related audio and ML dependencies

## Verification

Once the correct Python installation was in place:

- the project virtual environment worked
- **torch 2.7.1+cu118** and **coqui-tts 0.27.5** were installed
- the GPU check passed on the **RTX 4060**
- the project settings pointed to the expected input and output files

## Voice Reference and XTTS Run

The repository expected a reference WAV file in the `voices` folder. Once the reference file was added, the remaining XTTS workflow was completed.

During this phase, a compatibility issue in the XTTS setup was addressed by updating:

- `run_xtts.py`
- `requirements_xtts.txt`
- `settings.json`

The session also required acceptance of Coqui’s non-commercial CPML terms before the XTTS model could download. After that, the model downloaded successfully and the project generated the output file:

- `tim_test_xtts.wav`

Synthesis completed successfully on the GPU using the provided reference audio.

## Final Outcome

At the end of the setup, the repository was left in a working state with:

- a functioning Python 3.11 virtual environment
- working PyTorch CUDA support
- installed XTTS dependencies
- a reference voice workflow
- a generated XTTS output file
- updated README notes documenting the working configuration and compatibility fixes

## Tools and Technologies

- **Windows PowerShell**
- **Python 3.11.9**
- **Virtual Environment (`.venv`)**
- **PyTorch 2.7.1 + cu118**
- **torchvision / torchaudio**
- **coqui-tts 0.27.5**
- **XTTS voice cloning**
- **NVIDIA RTX 4060 GPU**

## Summary

This project established a reproducible local XTTS voice cloning setup for Windows. The main work involved correcting the Python environment, creating a dedicated virtual environment, installing the necessary machine learning and audio packages, resolving compatibility issues, and successfully generating a test voice output from a reference WAV file. The result is a working local TTS project that can be reused and extended for future experiments.
