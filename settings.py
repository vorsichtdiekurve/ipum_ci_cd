from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    hf_model_name: str = "bardsai/twitter-sentiment-pl-base"
    local_model_name: str = "twitter-sentiment-pl-base"
    model_path: str = "artifacts/model"
    tokenizer_path: str = "artifacts/tokenizer"
    onnx_model_path: str = "artifacts/onnx"
    onnx_model_name: str = "twitter-sentiment-pl-base.onnx"


settings = Settings()
