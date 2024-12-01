from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct, Distance

from call_llm import generate_embeddings

import os
from dotenv import load_dotenv
from pathlib import Path

import pandas as pd

# Load environment variables
load_dotenv(dotenv_path=Path("../../.env"))

QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_HOST = os.environ.get("QDRANT_HOST")

model = None

# Qdrant cloud client initialization
qdrant_client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)


# Function to create a Qdrant collection
def create_collection(collection_name, size=768):
    collection_exists = qdrant_client.collection_exists(collection_name)
    if collection_exists:
        print(f"Skipping collection `{collection_name}` creation as it already exists.")
    else:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )


# Function to upload vectors to Qdrant
def upload_vectors(listing_id, vectors, collection_name):
    # Prepare and insert points into the collection
    points = [
        PointStruct(
            id=int(listing_id),
            vector=vector.tolist(),
            # payload=metadata[idx]
        )
        for idx, vector in enumerate(vectors)
    ]

    qdrant_client.upsert(collection_name=collection_name, points=points)


def process_listing(id, content, collection_name, model_origin):
    if model_origin == "huggingface":
        doc_vectors = model.encode([content], convert_to_tensor=True)
    elif model_origin == "gemini":
        doc_vectors = generate_embeddings(content)
    else:
        raise ValueError("Unknown `model_origin` parameter")

    # Upload vectors
    upload_vectors(id, doc_vectors, collection_name)


def create_vectors(df, collection_name, model_origin="gemini"):
    """
    model_origin = huggingface (for self host) or gemini
    """
    if model_origin == "huggingface":
        from sentence_transformers import SentenceTransformer
        global model
        model = SentenceTransformer(
            "stjiris/bert-large-portuguese-cased-legal-mlm-nli-sts-v1"
        )
    df = (
        df.drop("Pictures", axis=1)
        .drop_duplicates("Listing ID")
        .rename(
            columns={
                "Region": "Região",
                "Name": "Nome",
                "Title": "Título",
                "Room Type": "Tipo de Hospedagem",
                "Person Capacity": "Capacidade de Pessoas",
                "Price per Night (R$)": "Preço por Noite (R$)",
                "Rating": "Nota",
                "Reviews": "Avaliações",
                "Badge": "Selo",
                "Description": "Descrição",
                "Amenities": "Comodidades",
            }
        )
    )
    for idx, listing in df.iterrows():
        listing_id = listing["Listing ID"]
        content = str(listing.drop("Listing ID").dropna().to_dict())
        process_listing(listing_id, content, collection_name, model_origin)


if __name__ == "__main__":
    # create_collection("listings", 1024)
    create_collection("listings_gemini", 768)
    df = pd.read_csv("../../data/airbnb_data.csv")
    # create_vectors(df, collection_name="listings", model_origin="huggingface")
    create_vectors(df, collection_name="listings_gemini", model_origin="gemini")
