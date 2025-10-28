#!/bin/sh
set -e

PORT=8080

export GOOGLE_GENAI_USE_VERTEXAI=FALSE

echo "Starting ADK agent in port $PORT"
uvicorn main:app --host 0.0.0.0 --port "${PORT}"
