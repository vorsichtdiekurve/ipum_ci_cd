import os
import onnxruntime as ort
from settings import Settings
from tokenizers import Tokenizer


def load_onnx_model(settings: Settings):
    tok_json = os.path.join(settings.tokenizer_path, "tokenizer.json")
    if not os.path.isfile(tok_json):
        raise FileNotFoundError(f"No tokenizer.json at {tok_json}")
    tokenizer = Tokenizer.from_file(tok_json)

    onnx_model_path = os.path.join(settings.onnx_model_path, settings.onnx_model_name)
    if not os.path.exists(onnx_model_path):
        raise FileNotFoundError(
            f"ONNX model path {settings.onnx_model_path} does not exist."
        )
    session = ort.InferenceSession(onnx_model_path)

    return session, tokenizer
