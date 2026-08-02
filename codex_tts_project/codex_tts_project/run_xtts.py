import json
from pathlib import Path

import torch
from packaging.version import Version

import transformers.pytorch_utils as hf_pytorch_utils
import transformers.utils.import_utils as hf_import_utils

# Coqui XTTS currently straddles old and new transformers APIs.
# Patch the missing helpers locally instead of editing site-packages.
if not hasattr(hf_import_utils, "is_torch_greater_or_equal"):
    def is_torch_greater_or_equal(version: str) -> bool:
        return Version(torch.__version__.split("+", maxsplit=1)[0]) >= Version(version)

    hf_import_utils.is_torch_greater_or_equal = is_torch_greater_or_equal

if not hasattr(hf_import_utils, "is_torchcodec_available"):
    def is_torchcodec_available() -> bool:
        return False

    hf_import_utils.is_torchcodec_available = is_torchcodec_available

if not hasattr(hf_pytorch_utils, "isin_mps_friendly"):
    def isin_mps_friendly(*, elements, test_elements):
        return torch.isin(elements, test_elements)

    hf_pytorch_utils.isin_mps_friendly = isin_mps_friendly

from TTS.api import TTS

ROOT = Path(__file__).resolve().parent

# These are starting points for repeatable delivery variations. Individual
# settings in settings.json override the selected preset when needed.
PRESETS = {
    "focused": {
        "temperature": 0.35,
        "top_p": 0.75,
        "top_k": 30,
        "repetition_penalty": 7.0,
    },
    "natural": {
        "temperature": 0.75,
        "top_p": 0.85,
        "top_k": 50,
        "repetition_penalty": 5.0,
    },
    "expressive": {
        "temperature": 0.95,
        "top_p": 0.95,
        "top_k": 100,
        "repetition_penalty": 3.0,
    },
}
settings_path = ROOT / "settings.json"
if not settings_path.exists():
    settings_path = ROOT / "settings.example.json"

with open(settings_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

text_file = cfg.get("text_file")
if text_file:
    text_path = ROOT / text_file
    text = text_path.read_text(encoding="utf-8").strip()
else:
    text = cfg["text"]

language = cfg.get("language", "en")
speaker_source = ROOT / cfg["speaker_wav"]
if speaker_source.is_dir():
    supported_audio = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
    speaker_wav = sorted(
        path for path in speaker_source.iterdir()
        if path.is_file() and path.suffix.lower() in supported_audio
    )
    if not speaker_wav:
        raise ValueError(f"No supported reference audio found in: {speaker_source}")
else:
    speaker_wav = [speaker_source]

output_wav = ROOT / cfg["output_wav"]
model_name = cfg.get("model_name", "tts_models/multilingual/multi-dataset/xtts_v2")
speed = cfg.get("speed", 1.0)
preset_name = cfg.get("preset", "natural")
if preset_name not in PRESETS:
    available = ", ".join(PRESETS)
    raise ValueError(f"Unknown preset '{preset_name}'. Choose one of: {available}")

generation = PRESETS[preset_name].copy()
for option in generation:
    if option in cfg:
        generation[option] = cfg[option]

seed = cfg.get("seed")
if seed is not None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

output_wav.parent.mkdir(parents=True, exist_ok=True)

print(f"Loading model: {model_name}")
tts = TTS(model_name=model_name)

print(f"Generating audio from {len(speaker_wav)} reference file(s): {speaker_wav}")
print(f"Preset: {preset_name}; seed: {seed}; settings: {generation}")
tts.tts_to_file(
    text=text,
    speaker_wav=[str(path) for path in speaker_wav],
    language=language,
    speed=speed,
    file_path=str(output_wav),
    **generation,
)

print(f"Done. Output saved to: {output_wav}")
