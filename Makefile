.PHONY: init prepare_artifacts start init_docker

init:
	uv venv --python 3.13 && \
	. .venv/bin/activate
	uv sync --all-groups
	
prepare_artifacts:
	uv run python main.py --script download

export_model_to_onnx:
	uv run python main.py --script export

clean_model_artifacts:
	rm -rf artifacts/model

build_docker:
	make clean_model_artifacts
	uv run docker build -t polish-sentiment-app-onnx:latest .

run_ruff:
	uv run ruff check . --fix
	uv run ruff format .

run_pip_audit:
	uv run pip-audit --vulnerability-service pypi

run_tests:
	uv run pytest tests

start:
	uv run uvicorn app:app --reload --port 8000

start_docker:
	docker run --rm -ti -p 8000:8000 polish-sentiment-app-onnx:latest 