from dotenv import load_dotenv
from google import genai
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.genai import types
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

load_dotenv()

# Constants
MENU_FIRESTORE_COLLECTION = "menu"
DATABASE_NAME = "embeddings"
GEMINI_MODEL_EMBEDDING = "gemini-embedding-001"


def chunking(file_path: str) -> list:
    loader = TextLoader(file_path)
    documents = loader.load()

    headers_to_split_on = [("##", "MenuCategory")]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    chunks = markdown_splitter.split_text(documents[0].page_content)
    return chunks


def create_embeddings(chunk: Document) -> tuple:
    print("creating embeddings")
    try:
        text_content = f"{chunk.metadata.get('MenuCategory')} - {chunk.page_content}"

        client = genai.Client()
        result = client.models.embed_content(
            model=GEMINI_MODEL_EMBEDDING,
            contents=text_content,
            config=types.EmbedContentConfig(
                task_type="SEMANTIC_SIMILARITY",
                output_dimensionality=768,
            ),
        )

        return result, text_content
    except Exception as e:
        print(f"An error occurred in create_embeddings: {e}")
        raise e


def save_chunks_embeddings(chunks: list) -> None:
    print("embeddings created and saved to Firestore")
    db = firestore.Client(database=DATABASE_NAME)
    try:
        for chunk in chunks:
            result, text_content = create_embeddings(chunk)

            doc_ref = db.collection(MENU_FIRESTORE_COLLECTION).document()
            doc_ref.set(
                {
                    "text_content": text_content,
                    "embedding": Vector(result.embeddings[0].values),
                    "timestamp": firestore.SERVER_TIMESTAMP,
                }
            )

    except Exception as e:
        print(f"An error occurred in save_chunks_embeddings: {e}")
        return


# create a function that receive a path file and chunking a file using langchain, create embeddings using gemini and save the embedddings in firestore


def ingestion_menu(file_path: str) -> None:
    """
    Ingests a menu file by chunking it, creating embeddings using Gemini, and saving them to Firestore.

    Args:
        file_path (str): The path to the menu file.
    """
    chunking_menu = chunking(file_path)
    save_chunks_embeddings(chunking_menu)


if __name__ == "__main__":
    menu_file = "resources/menu.md"
    ingestion_menu(menu_file)
