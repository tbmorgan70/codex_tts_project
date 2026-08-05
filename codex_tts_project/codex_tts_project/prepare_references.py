Exit code: 0
Wall time: 0.5 seconds
Output:
"""Create conservative, non-destructive XTTS reference WAV files."""

import argparse
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfiltfilt


SUPPORTED_AUDIO = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
TARGET_SAMPLE_RATE = 24_000
HIGH_PASS_HZ = 70
TARGET_PEAK = 10 ** (-1 / 20)  # -1 dBFS


def prepare_file(source: Path, destination: Path) -> None:
    audio, _ = librosa.load(source, sr=TARGET_SAMPLE_RATE, mono=True)
    audio, _ = librosa.effects.trim(audio, top_db=40)
    if not len(audio):
        raise ValueError("No audible signal after trimming")

    # Remove subsonic rumble without changing the voice character.
    high_pass = butter(2, HIGH_PASS_HZ, btype="highpass", fs=TARGET_SAMPLE_RATE, output="sos")
    audio = sosfiltfilt(high_pass, audio).astype(np.float32)

    peak = float(np.max(np.abs(audio)))
    if peak:
        audio *= TARGET_PEAK / peak

    destination.parent.mkdir(parents=True, exist_ok=True)
    sf.write(destination, audio, TARGET_SAMPLE_RATE, subtype="PCM_16")
    print(f"Prepared {source.name} -> {destination.name} ({len(audio) / TARGET_SAMPLE_RATE:.1f}s)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    source_dir = args.source_dir.resolve()
    output_dir = (args.output_dir or source_dir / "prepared").resolve()
    sources = sorted(
        path for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO
    )
    if not sources:
        raise ValueError(f"No supported audio files found in: {source_dir}")

    for source in sources:
        prepare_file(source, output_dir / f"{source.stem}_xtts.wav")


if __name__ == "__main__":
    main()

