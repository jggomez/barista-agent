FROM python:3.10-slim as builder
RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --no-interaction --no-ansi
# Use a slim Python base image for a smaller final container
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /app/.venv/ .venv/
ENV PATH="/app/.venv/bin:$PATH"
# Copy the application code
COPY ./agents/barista_agent/ ./barista_agent/
COPY ./agents/images/ ./images/
COPY ./main.py .
# Copy and make the startup script executable
COPY start.sh .
RUN chmod +x start.sh
# Use the script to start both the toolbox and the agent
CMD ["./start.sh"]
