"""Embedding service for semantic similarity"""
from openai import OpenAI
from config import get_settings
import numpy as np

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


def get_embedding(text: str) -> list[float]:
    """Get embedding for text using OpenAI API"""
    if not client:
        # Return mock embedding if no API key (for demo)
        return [0.1] * 1536
    
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        # Return mock embedding on error
        return [0.1] * 1536


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    a_arr = np.array(a)
    b_arr = np.array(b)
    
    dot_product = np.dot(a_arr, b_arr)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(dot_product / (norm_a * norm_b))

