from pathlib import Path
import json
import shutil
from huggingface_hub import snapshot_download
from transformers import pipeline
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

SUPPORTED_LANGUAGES = {
    "en": "facebook/mms-tts-eng",
    "ru": "facebook/mms-tts-rus",
    "uk": "facebook/mms-tts-ukr",
    "pl": "facebook/mms-tts-pol",
    "de": "facebook/mms-tts-deu",
    "fr": "facebook/mms-tts-fra",
    "es": "facebook/mms-tts-spa",
    "it": "facebook/mms-tts-ita",
    "pt": "facebook/mms-tts-por",
    "zh": "facebook/mms-tts-cmn",
    "ja": "facebook/mms-tts-jpn",
    "ko": "facebook/mms-tts-kor",
    "ar": "facebook/mms-tts-ara",
    "hi": "facebook/mms-tts-hin",
    "tr": "facebook/mms-tts-tur",
    "nl": "facebook/mms-tts-nld",
    "sv": "facebook/mms-tts-swe",
    "fi": "facebook/mms-tts-fin",
    "da": "facebook/mms-tts-dan",
    "no": "facebook/mms-tts-nor",
    "cs": "facebook/mms-tts-ces",
    "sk": "facebook/mms-tts-slk",
    "hu": "facebook/mms-tts-hun",
    "ro": "facebook/mms-tts-ron",
    "bg": "facebook/mms-tts-bul",
    "el": "facebook/mms-tts-ell",
    "he": "facebook/mms-tts-heb",
    "th": "facebook/mms-tts-tha",
    "vi": "facebook/mms-tts-vie",
    "id": "facebook/mms-tts-ind"
}

def synthesize_speech(text: str, output_path: str, lang: str = "en", model_id: str = None):
    target_model = model_id if model_id else SUPPORTED_LANGUAGES.get(lang.lower())
    
    if not target_model:
        raise ValueError(f"Unsupported language code '{lang}'.")
        
    tts = pipeline("text-to-speech", model=target_model)
    result = tts(text)
    
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