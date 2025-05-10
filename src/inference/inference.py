import cleantext
import numpy as np

from settings import Settings
from .load_onnx_model import load_onnx_model


class Inference:
    CLASS_TO_STR_MAPPING = {"0": "positive", "1": "neutral", "2": "negative"}

    def __init__(self, settings: Settings):
        self.settings = settings
        self.session, self.tokenizer = load_onnx_model(settings)

    def _tokenize(self, text: str) -> tuple[np.ndarray, np.ndarray]:
        text = self._clean_text(text)
        enc = self.tokenizer.encode(text)
        input_ids = np.array([enc.ids], dtype=np.int64)
        attn = np.array([enc.attention_mask], dtype=np.int64)
        return input_ids, attn

    def _preprocess_text(self, text: str) -> dict:
        inputs, attn = self._tokenize(text)
        ort_inputs = {
            "input_ids": inputs.astype(np.int64),
            "attention_mask": attn.astype(np.int64),
        }
        return ort_inputs

    def _postprocess_text(self, logits: np.ndarray) -> list[str]:
        preds = np.argmax(logits, axis=-1)
        preds = [self.CLASS_TO_STR_MAPPING[str(pred)] for pred in preds]
        return preds

    @staticmethod
    def _clean_text(text: str) -> str:
        return cleantext.clean(
            text,
            to_ascii=False,
            lower=True,
            no_emoji=True,
            no_urls=True,
            no_emails=True,
            no_phone_numbers=True,
            replace_with_url=" ",
            replace_with_email=" ",
            replace_with_phone_number=" ",
        )

    def predict(self, text: str) -> list[str]:
        inputs = self._preprocess_text(text)
        ort_outs = self.session.run(None, inputs)
        logits = ort_outs[0]
        return self._postprocess_text(logits)
