"""Cross-encoder reranking for better result ordering"""
from sentence_transformers import CrossEncoder
from typing import List, Dict, Tuple
from functools import lru_cache


@lru_cache(maxsize=1)
def get_reranker_model():
    """Load and cache cross-encoder model"""
    print("Loading cross-encoder model...")
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    print("Reranker model loaded!")
    return model


class Reranker:
    """Rerank search results using cross-encoder"""
    
    def __init__(self):
        """Initialize reranker"""
        self.model = None
    
    def _ensure_model(self):
        """Lazy load model on first use"""
        if self.model is None:
            self.model = get_reranker_model()
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = None
    ) -> List[Tuple[int, float]]:
        """Rerank documents by relevance to query
        
        Args:
            query: Search query
            documents: List of document texts
            top_k: Number of top results to return (None = all)
            
        Returns:
            List of (original_index, score) tuples, sorted by score
        """
        if not documents:
            return []
        
        self._ensure_model()
        
        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]
        
        # Get relevance scores
        scores = self.model.predict(pairs)
        
        # Create (index, score) tuples
        results = [(i, float(score)) for i, score in enumerate(scores)]
        
        # Sort by score (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k if specified
        if top_k:
            results = results[:top_k]
        
        return results
    
    def rerank_with_metadata(
        self,
        query: str,
        results: List[Dict],
        text_key: str = "text",
        top_k: int = None
    ) -> List[Dict]:
        """Rerank results that include metadata
        
        Args:
            query: Search query
            results: List of result dicts
            text_key: Key in dict that contains text
            top_k: Number of results to return
            
        Returns:
            Reranked list of result dicts with added 'rerank_score'
        """
        if not results:
            return []
        
        # Extract documents
        documents = [r.get(text_key, "") for r in results]
        
        # Get reranked indices and scores
        reranked = self.rerank(query, documents, top_k=top_k)
        
        # Build reranked results
        reranked_results = []
        for idx, score in reranked:
            result = results[idx].copy()
            result['rerank_score'] = score
            reranked_results.append(result)
        
        return reranked_results
    
    def score_pairs(
        self,
        query_doc_pairs: List[Tuple[str, str]]
    ) -> List[float]:
        """Score multiple query-document pairs
        
        Args:
            query_doc_pairs: List of (query, document) tuples
            
        Returns:
            List of relevance scores
        """
        if not query_doc_pairs:
            return []
        
        self._ensure_model()
        
        # Convert to list of lists
        pairs = [[q, d] for q, d in query_doc_pairs]
        
        # Get scores
        scores = self.model.predict(pairs)
        
        return [float(s) for s in scores]


# Global instance
_reranker = None


def get_reranker() -> Reranker:
    """Get or create reranker singleton"""
    global _reranker
    if _reranker is None:
        _reranker = Reranker()
    return _reranker

