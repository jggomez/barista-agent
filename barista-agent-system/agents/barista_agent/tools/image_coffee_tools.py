import os
import uuid
from io import BytesIO

from dotenv import load_dotenv
from google import genai
from google.cloud import storage
from google.genai import types
from PIL import Image

load_dotenv()

MODEL_IMAGEN = os.getenv("MODEL_IMAGEN")

if not MODEL_IMAGEN:
    raise ValueError("The MODEL_IMAGEN environment variable is not set.")

PROJECT_ID = os.getenv("PROJECT_ID")

if not PROJECT_ID:
    raise ValueError("The PROJECT_ID environment variable is not set.")

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

if not BUCKET_NAME:
    raise ValueError("The GCS_BUCKET_NAME environment variable is not set.")


def create_image_coffee(coffee_image_prompt: str) -> str | None:
    """
    Generates an image of a coffee based on the provided prompt.

    Args:
        coffee_image_prompt (str): The prompt describing the coffee image to generate.

    Returns:
        str | None: The URL or base64 encoded string of the generated image, or None if an error occurs.
    """
    try:
        client = genai.Client()

        response = client.models.generate_images(
            model=MODEL_IMAGEN,
            prompt=coffee_image_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            ),
        )

        if response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes

            image = Image.open(BytesIO(image_bytes))
            image.save("images/coffee_image.png")

            storage_client = storage.Client(project=PROJECT_ID)
            bucket = storage_client.bucket(BUCKET_NAME)

            file_name = f"image-{uuid.uuid4()}.png"
            blob = bucket.blob(file_name)

            print(f"Uploading CSV to gs://{BUCKET_NAME}/{file_name}")
            blob.upload_from_string(image_bytes, content_type="image/png")

            url = f"https://storage.googleapis.com/{BUCKET_NAME}/{file_name}"
            print(f"Successfully uploaded to {url}")
            return url

        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
