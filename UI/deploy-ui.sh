#!/bin/bash
set -e

PROJECT_ID="devhack-3f0c2"

SERVICE_ACCOUNT="agents@${PROJECT_ID}.iam.gserviceaccount.com"

SERVICE_NAME="barista-agent-ui"

REGION="us-central1"

IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Building agent UI Docker image: ${IMAGE_NAME}"
gcloud builds submit --tag "${IMAGE_NAME}" . --project "${PROJECT_ID}"

echo "Deploying agent UI to Cloud Run service: ${SERVICE_NAME}"
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_NAME}" \
    --service-account "${SERVICE_ACCOUNT}" \
    --update-env-vars=AGENT_URL_BASE=https://barista-agent-823002731253.us-central1.run.app \
    --platform "managed" \
    --region "${REGION}" \
    --allow-unauthenticated \
    --project "${PROJECT_ID}"

SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform "managed" --region "${REGION}" --project "${PROJECT_ID}" --format="value(status.url)")

echo -e "\nAgent UI deployment successful!"
echo "Your agent UI is available at: ${SERVICE_URL}"
