from typing import List

from dotenv import load_dotenv
from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector
from google.genai import types

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Constants
MENU_FIRESTORE_COLLECTION = "menu"
DATABASE_NAME = "embeddings"
GEMINI_MODEL_EMBEDDING = "gemini-embedding-001"


def get_menu_items(type_coffee: str) -> List[str]:
    """
    Returns a list of menu items based on the type of coffee.

    Args:
        type_coffee (str): The type of coffee to search for.

    Returns:
        List[str]: A list of menu items.
    """

    try:
        db = firestore.Client(database=DATABASE_NAME)

        client = genai.Client()

        print("creating embeddings...")

        result = client.models.embed_content(
            model=GEMINI_MODEL_EMBEDDING,
            contents=type_coffee,
            config=types.EmbedContentConfig(
                task_type="SEMANTIC_SIMILARITY",
                output_dimensionality=768,
            ),
        )

        embeddings_collection = db.collection(MENU_FIRESTORE_COLLECTION)

        vector_query = embeddings_collection.find_nearest(
            vector_field="embedding",
            query_vector=Vector(result.embeddings[0].values),
            distance_measure=DistanceMeasure.COSINE,
            limit=2,
        )

        docs = vector_query.stream()
        print("Getting menu items...")

        menu_items = []

        for doc in docs:
            print(doc.get("text_content"))
            menu_items.append(doc.get("text_content"))

        return menu_items

    except Exception as e:
        print(f"An error occurred in get_menu_items: {e}")
        return []
