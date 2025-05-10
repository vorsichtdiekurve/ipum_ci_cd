import os
from settings import Settings
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def export_model_to_onnx(settings: Settings):
    model = AutoModelForSequenceClassification.from_pretrained(settings.model_path)
    tokenizer = AutoTokenizer.from_pretrained(settings.tokenizer_path)

    model.eval()
    dummy_text = "This is a sample input for ONNX export."
    inputs = tokenizer(dummy_text, return_tensors="pt")

    onnx_path = os.path.join(settings.onnx_model_path, settings.onnx_model_name)
    os.makedirs(settings.onnx_model_path, exist_ok=True)

    with torch.no_grad():
        torch.onnx.export(
            model,
            (inputs["input_ids"], inputs.get("attention_mask")),
            onnx_path,
            input_names=["input_ids", "attention_mask"],
            output_names=["logits"],
            dynamic_axes={
                "input_ids": {0: "batch_size", 1: "sequence"},
                "attention_mask": {0: "batch_size", 1: "sequence"},
                "logits": {0: "batch_size"},
            },
            opset_version=14,
        )

    print(f"ONNX model exported to {onnx_path}")
    return onnx_path
