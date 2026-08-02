# Changelog

All notable workflow changes are documented here.

## v0.2.0 - 2026-08-01

### Added

- File-based scripts through the optional `text_file` setting.
- `speed` control for faster or slower output.
- Three named generation presets: `focused`, `natural`, and `expressive`.
- Optional `seed` for repeatable comparison renders.
- Multi-reference voice input: `speaker_wav` can now be one audio file or a folder of WAV, MP3, FLAC, M4A, and OGG clips.
- `docs/VOICE_WORKFLOW.md` with reference preparation and generation guidance.

### Changed

- `run_xtts.py` passes selected generation controls to XTTS and reports the chosen reference files, preset, seed, and settings.
- `settings.example.json` now documents the current workflow controls.

### Validated

- Generated focused, natural, and expressive takes from one text using the same five-reference voice folder, fixed seed, and speed.