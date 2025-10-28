#!/bin/bash
set -e

PROJECT_ID="devhack-3f0c2"

AGENT_SERVICE_ACCOUNT="agents@${PROJECT_ID}.iam.gserviceaccount.com"

# Cloud Run service name for the AGENT
AGENT_SERVICE_NAME="barista-agent"

REGION="us-central1"

# Docker image name for the agent
AGENT_IMAGE_NAME="gcr.io/${PROJECT_ID}/${AGENT_SERVICE_NAME}"

# --- Build and Deploy Agent ---
echo "Building agent Docker image: ${AGENT_IMAGE_NAME}"
gcloud builds submit --tag "${AGENT_IMAGE_NAME}" . --project "${PROJECT_ID}"

echo "Deploying agent to Cloud Run service: ${AGENT_SERVICE_NAME}"
gcloud run deploy "${AGENT_SERVICE_NAME}" \
    --image "${AGENT_IMAGE_NAME}" \
    --service-account "${AGENT_SERVICE_ACCOUNT}" \
    --update-secrets GOOGLE_API_KEY=GOOGLE_GENAI_API_KEY:latest \
    --update-env-vars=GOOGLE_GENAI_USE_VERTEXAI=FALSE \
    --update-env-vars=GOOGLE_CLOUD_PROJECT=${PROJECT_ID} \
    --update-env-vars=LLM_AGENT=gemini-2.5-flash \
    --update-env-vars=PROJECT_ID=${PROJECT_ID} \
    --update-env-vars=GCS_BUCKET_NAME=barista-agent \
    --update-env-vars=MODEL_IMAGEN=imagen-4.0-generate-001 \
    --platform "managed" \
    --region "${REGION}" \
    --allow-unauthenticated \
    --project "${PROJECT_ID}"

AGENT_SERVICE_URL=$(gcloud run services describe "${AGENT_SERVICE_NAME}" --platform "managed" --region "${REGION}" --project "${PROJECT_ID}" --format="value(status.url)")

echo -e "\nAgent deployment successful!"
echo "Your agent is available at: ${AGENT_SERVICE_URL}"
