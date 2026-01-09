"""Vector store using ChromaDB for semantic search"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os


class VectorStore:
    """ChromaDB wrapper for message embeddings"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client with persistence"""
        self.persist_directory = persist_directory
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize client with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="messages",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        print(f"Vector store initialized: {self.collection.count()} documents")
    
    def store(
        self,
        id: str,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict] = None
    ) -> None:
        """Store a document with its embedding
        
        Args:
            id: Unique document ID
            text: Original text content
            embedding: Pre-computed embedding vector
            metadata: Optional metadata (sender_type, timestamp, etc.)
        """
        self.collection.add(
            ids=[id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else None
        )
    
    def store_batch(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict]] = None
    ) -> None:
        """Store multiple documents at once"""
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """Search for similar documents
        
        Args:
            query_embedding: Query vector
            n_results: Number of results to return
            where: Filter conditions (e.g., {"sender_type": "investor"})
            
        Returns:
            Dict with ids, documents, distances, metadatas
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return {
            "ids": results["ids"][0] if results["ids"] else [],
            "documents": results["documents"][0] if results["documents"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else []
        }
    
    def get(self, id: str) -> Optional[Dict]:
        """Get a document by ID"""
        try:
            result = self.collection.get(ids=[id])
            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "document": result["documents"][0],
                    "metadata": result["metadatas"][0] if result["metadatas"] else None
                }
        except Exception:
            pass
        return None
    
    def delete(self, id: str) -> None:
        """Delete a document by ID"""
        self.collection.delete(ids=[id])
    
    def reset(self) -> None:
        """Clear all documents"""
        self.client.delete_collection(name="messages")
        self.collection = self.client.create_collection(
            name="messages",
            metadata={"hnsw:space": "cosine"}
        )
        print("Vector store reset complete")
    
    def count(self) -> int:
        """Get total document count"""
        return self.collection.count()


# Global instance
_vector_store = None


def get_vector_store() -> VectorStore:
    """Get or create vector store singleton"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

