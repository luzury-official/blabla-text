from pathlib import Path
import json
import shutil
from huggingface_hub import snapshot_download
from transformers import pipeline, AutoProcessor
import scipy.io.wavfile as wav

def get_config_dir(app_name="BlaBla-Text"):
    home = Path.home()
    config_dir = home / f".{app_name.lower()}"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

CONFIG_FILE = get_config_dir() / "config.json"

def save_settings(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_settings():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Bark - одна мультиязычная модель, без отдельного чекпоинта на каждый язык.
# bark-small быстрее и легче, bark (полная версия) звучит качественнее.
DEFAULT_MODEL = "suno/bark-small"

RECOMMENDED_MODELS = {
    "bark-small (быстрее, слабее качество)": "suno/bark-small",
    "bark (медленнее, качество выше)": "suno/bark",
}

# Языки, под которые у Bark есть готовые голосовые пресеты (v2/<lang>_speaker_<0-9>)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "tr": "Turkish",
    "zh": "Chinese",
}

def build_voice_preset(lang: str, speaker: int = 6) -> str:
    lang = lang.lower()
    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language code '{lang}'.")
    if not 0 <= speaker <= 9:
        raise ValueError("Speaker index must be between 0 and 9.")
    return f"v2/{lang}_speaker_{speaker}"

def synthesize_speech(text: str, output_path: str, lang: str = "en", model_id: str = None, speaker: int = 6):
    target_model = model_id if model_id else DEFAULT_MODEL
    voice_preset = build_voice_preset(lang, speaker)

    processor = AutoProcessor.from_pretrained(target_model)
    history_prompt = processor(".", voice_preset=voice_preset)["history_prompt"]

    tts = pipeline("text-to-speech", model=target_model)
    result = tts(text, forward_params={"history_prompt": history_prompt, "do_sample": True})

    audio_data = result["audio"]
    if audio_data.ndim > 1:
        audio_data = audio_data[0]

    wav.write(output_path, result["sampling_rate"], audio_data)

def get_installed_models():
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    installed = []

    if cache_dir.exists():
        for item in cache_dir.iterdir():
            if item.is_dir() and item.name.startswith("models--"):
                model_name = item.name.replace("models--", "").replace("--", "/")
                installed.append(model_name)

    return installed

def download_model(model_name: str):
    snapshot_download(repo_id=model_name)

def delete_model(model_name: str):
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    folder_name = "models--" + model_name.replace("/", "--")
    model_path = cache_dir / folder_name

    if model_path.exists() and model_path.is_dir():
        shutil.rmtree(model_path)
        return True
    return False