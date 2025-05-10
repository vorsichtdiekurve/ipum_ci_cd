import os
from settings import Settings
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def download_model(settings: Settings):
    model_name = settings.hf_model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return model, tokenizer


def save_model(settings: Settings, model, tokenizer):
    os.makedirs(settings.model_path, exist_ok=True)
    os.makedirs(settings.tokenizer_path, exist_ok=True)
    model.save_pretrained(settings.model_path)
    tokenizer.save_pretrained(settings.tokenizer_path)


def download_artifacts(settings: Settings):
    model, tokenizer = download_model(settings)
    save_model(settings, model, tokenizer)
