# Voice Workflow

## Reference Preparation

Use recordings you are authorized to use for voice cloning.

For a given voice, begin with two to five clips that are:

- Clear, single-speaker speech with no music, overlapping speakers, or heavy effects.
- Consistent in tone and recording environment.
- About 6-15 seconds each. A small curated set is more useful than one long, mixed recording.
- Free of long silence, clipped audio, strong reverb, and aggressive compression.

The runner accepts a single audio path or a folder. Folder input uses supported audio files in filename order:

`*.wav`, `*.mp3`, `*.flac`, `*.m4a`, `*.ogg`

Do not heavily denoise, gate, compress, or EQ references. Light repair is appropriate only when it removes a clear defect such as low-frequency rumble or persistent background noise.

## Configuration

Start from `settings.example.json`.

```json
{
  "text_file": "input/my_script.txt",
  "language": "en",
  "speed": 1.0,
  "preset": "natural",
  "seed": 42,
  "speaker_wav": "voices/my_voice",
  "output_wav": "output/my_voice_take.wav"
}
```

Use `text_file` for scripts. If it is absent, the runner falls back to the inline `text` value.

## Delivery Presets

| Preset | Intended use | Temperature | Top-p | Top-k | Repetition penalty |
| --- | --- | ---: | ---: | ---: | ---: |
| `focused` | Tighter, more controlled takes | 0.35 | 0.75 | 30 | 7.0 |
| `natural` | Balanced default | 0.75 | 0.85 | 50 | 5.0 |
| `expressive` | More animated variations | 0.95 | 0.95 | 100 | 3.0 |

A fixed `seed` makes comparison renders more repeatable. Use the same voice set, text, speed, and seed when evaluating presets.

The four sampling values may be supplied directly in `settings.json` to override the selected preset:

```json
{
  "preset": "natural",
  "temperature": 0.65,
  "top_p": 0.9,
  "top_k": 60,
  "repetition_penalty": 4.5
}
```

## Practical Iteration

1. Make a natural-speed `natural` baseline.
2. Render `focused` and `expressive` with the same seed.
3. Choose the closest take before changing more than one thing.
4. Adjust speed only after selecting a delivery style.
5. Keep output filenames descriptive, including voice, text, preset, speed, and seed.

## Run

```powershell
$env:COQUI_TOS_AGREED = "1"
.\.venv\Scripts\python.exe run_xtts.py
```

The runner prints the chosen reference files and generation settings before it synthesizes.