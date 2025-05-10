FROM python:3.13-slim-bookworm as builder

WORKDIR /app

RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --group inference

FROM python:3.13-slim-bookworm AS runtime

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv

COPY settings.py settings.py
COPY app.py app.py
COPY src/ ./src/
COPY artifacts/onnx/twitter-sentiment-pl-base.onnx ./artifacts/onnx/twitter-sentiment-pl-base.onnx
COPY artifacts/tokenizer/tokenizer.json ./artifacts/tokenizer/tokenizer.json

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
