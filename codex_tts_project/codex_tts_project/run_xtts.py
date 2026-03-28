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
settings_path = ROOT / "settings.json"
if not settings_path.exists():
    settings_path = ROOT / "settings.example.json"

with open(settings_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

text = cfg["text"]
language = cfg.get("language", "en")
speaker_wav = ROOT / cfg["speaker_wav"]
output_wav = ROOT / cfg["output_wav"]
model_name = cfg.get("model_name", "tts_models/multilingual/multi-dataset/xtts_v2")

output_wav.parent.mkdir(parents=True, exist_ok=True)

print(f"Loading model: {model_name}")
tts = TTS(model_name=model_name)

print(f"Generating audio from speaker WAV: {speaker_wav}")
tts.tts_to_file(
    text=text,
    speaker_wav=str(speaker_wav),
    language=language,
    file_path=str(output_wav),
)

print(f"Done. Output saved to: {output_wav}")
