"""BM25 keyword search for exact term matching"""
from rank_bm25 import BM25Okapi
from typing import List, Dict, Tuple
import re


class KeywordSearcher:
    """BM25-based keyword search for messages"""
    
    def __init__(self):
        """Initialize BM25 searcher"""
        self.bm25 = None
        self.corpus = []
        self.metadata = []
        self.tokenized_corpus = []
    
    def index_messages(self, messages: List[Dict]) -> None:
        """Index messages for keyword search
        
        Args:
            messages: List of dicts with 'id', 'content', and metadata
        """
        self.corpus = []
        self.metadata = []
        self.tokenized_corpus = []
        
        for msg in messages:
            # Combine subject and content
            text = ""
            if msg.get("subject"):
                text += msg["subject"] + " "
            text += msg.get("content", "")
            
            # Store full text
            self.corpus.append(text)
            
            # Store metadata
            self.metadata.append({
                "id": msg.get("id"),
                "sender_name": msg.get("sender_name"),
                "sender_type": msg.get("sender_type"),
                "channel": msg.get("channel"),
                "timestamp": msg.get("timestamp")
            })
            
            # Tokenize for BM25
            tokens = self._tokenize(text)
            self.tokenized_corpus.append(tokens)
        
        # Build BM25 index
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
            print(f"BM25 index built: {len(self.corpus)} documents")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_sender_type: str = None
    ) -> List[Tuple[str, float, Dict]]:
        """Search for documents matching query
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_sender_type: Optional filter by sender_type
            
        Returns:
            List of (doc_id, score, metadata) tuples
        """
        if not self.bm25:
            return []
        
        # Tokenize query
        tokenized_query = self._tokenize(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)
        
        # Create results list
        results = []
        for i, score in enumerate(scores):
            if score > 0:  # Only include matches
                meta = self.metadata[i]
                
                # Apply filter if specified
                if filter_sender_type and meta.get("sender_type") != filter_sender_type:
                    continue
                
                results.append((
                    meta["id"],
                    float(score),
                    meta
                ))
        
        # Sort by score and return top-k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for BM25
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation except for important ones
        text = re.sub(r'[^\w\s\-@.]', ' ', text)
        
        # Split into words
        tokens = text.split()
        
        # Remove very short tokens
        tokens = [t for t in tokens if len(t) > 1]
        
        return tokens
    
    def get_term_frequencies(self, query: str) -> Dict[str, int]:
        """Get term frequencies for query terms in corpus
        
        Args:
            query: Query string
            
        Returns:
            Dict mapping terms to document frequencies
        """
        tokens = self._tokenize(query)
        term_freqs = {}
        
        for term in tokens:
            count = sum(1 for doc in self.tokenized_corpus if term in doc)
            term_freqs[term] = count
        
        return term_freqs


# Global instance
_keyword_searcher = None


def get_keyword_searcher() -> KeywordSearcher:
    """Get or create keyword searcher singleton"""
    global _keyword_searcher
    if _keyword_searcher is None:
        _keyword_searcher = KeywordSearcher()
    return _keyword_searcher

