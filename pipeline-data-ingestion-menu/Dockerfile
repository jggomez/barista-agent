FROM python:3.10-slim as builder
RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --no-interaction --no-ansi
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /app/.venv/ .venv/
ENV PATH="/app/.venv/bin:$PATH"
COPY ./src/ingestion_menu.py .
CMD ["python3", "ingestion_menu.py"]
