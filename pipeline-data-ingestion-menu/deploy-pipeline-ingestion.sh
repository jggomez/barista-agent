#!/bin/bash
set -e

PROJECT_ID="devhack-3f0c2"
PROJECT_NUMBER="823002731253"
AGENT_SERVICE_ACCOUNT="agents@${PROJECT_ID}.iam.gserviceaccount.com"
SERVICE_NAME="pipeline-data-ingestion"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
BUCKET="pipeline-rag-barista"


# --- Build and Deploy Agent ---
echo "Building agent Docker image: ${IMAGE_NAME}"
gcloud builds submit --tag "${IMAGE_NAME}" . --project "${PROJECT_ID}"

echo "Deploying agent to Cloud Run service: ${SERVICE_NAME}"
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_NAME}" \
    --service-account "${AGENT_SERVICE_ACCOUNT}" \
    --update-secrets GOOGLE_API_KEY=GOOGLE_GENAI_API_KEY:latest \
    --platform "managed" \
    --region "${REGION}" \
    --allow-unauthenticated \
    --project "${PROJECT_ID}"

URL=$(gcloud run services describe "${SERVICE_NAME}" --platform "managed" --region "${REGION}" --project "${PROJECT_ID}" --format="value(status.url)")

echo -e "\Pipeline deployment successful!"
echo "Your pipeline is available at: ${URL}"

gcloud eventarc triggers create event-storage-pipeline-barista \
    --location="${REGION}" \
    --service-account="${AGENT_SERVICE_ACCOUNT}" \
    --event-data-content-type=application/json \
    --destination-run-service="${SERVICE_NAME}" \
    --destination-run-region="${REGION}" \
    --destination-run-path="/" \
    --event-filters="bucket=${BUCKET}" \
    --event-filters="type=google.cloud.storage.object.v1.finalized"
