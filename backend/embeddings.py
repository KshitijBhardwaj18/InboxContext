"""Embedding service for semantic similarity"""
from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache

# Load model once and cache it
@lru_cache(maxsize=1)
def get_model():
    """Load and cache the embedding model"""
    print("Loading sentence-transformers model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded successfully!")
    return model


def get_embedding(text: str) -> list[float]:
    """Get embedding for text using local sentence-transformers model
    
    Model: all-MiniLM-L6-v2
    - Dimensions: 384
    - Fast inference (~0.01s per text)
    - Good for semantic search
    """
    if not text or not text.strip():
        # Return zero vector for empty text
        return [0.0] * 384
    
    try:
        model = get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception as e:
        print(f"Embedding error: {e}")
        # Return zero vector on error
        return [0.0] * 384


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

