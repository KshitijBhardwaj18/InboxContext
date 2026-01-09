"""Unified hybrid retriever combining multiple search strategies"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from embeddings import get_embedding
from vector_store import get_vector_store
from keyword_search import get_keyword_searcher
from reranker import get_reranker
from models import Decision, Message


class HybridRetriever:
    """Combine vector, graph, and keyword search with reranking"""
    
    def __init__(self, db: Session):
        """Initialize retriever
        
        Args:
            db: Database session
        """
        self.db = db
        self.vector_store = get_vector_store()
        self.keyword_searcher = get_keyword_searcher()
        self.reranker = get_reranker()
    
    def retrieve(
        self,
        query: str,
        sender_type: Optional[str] = None,
        top_k: int = 5,
        use_vector: bool = True,
        use_keyword: bool = True,
        use_graph: bool = True,
        rerank: bool = True
    ) -> List[Dict]:
        """Hybrid retrieval with multiple strategies
        
        Args:
            query: Search query
            sender_type: Filter by sender type
            top_k: Final number of results
            use_vector: Use semantic vector search
            use_keyword: Use BM25 keyword search
            use_graph: Use graph-based precedent
            rerank: Apply cross-encoder reranking
            
        Returns:
            List of ranked results with scores and sources
        """
        all_results = []
        
        # 1. Vector Search (Semantic)
        if use_vector:
            vector_results = self._vector_search(query, sender_type, n=top_k*2)
            all_results.extend(vector_results)
        
        # 2. Keyword Search (Lexical)
        if use_keyword:
            keyword_results = self._keyword_search(query, sender_type, n=top_k*2)
            all_results.extend(keyword_results)
        
        # 3. Graph Search (Precedent)
        if use_graph and sender_type:
            graph_results = self._graph_search(sender_type, n=top_k)
            all_results.extend(graph_results)
        
        # Deduplicate by ID
        seen_ids = set()
        unique_results = []
        for result in all_results:
            if result["id"] not in seen_ids:
                seen_ids.add(result["id"])
                unique_results.append(result)
        
        # Rerank if enabled
        if rerank and unique_results:
            unique_results = self.reranker.rerank_with_metadata(
                query=query,
                results=unique_results,
                text_key="text",
                top_k=top_k
            )
        else:
            # Just take top-k by original scores
            unique_results = sorted(
                unique_results,
                key=lambda x: x.get("score", 0),
                reverse=True
            )[:top_k]
        
        return unique_results
    
    def _vector_search(
        self,
        query: str,
        sender_type: Optional[str],
        n: int
    ) -> List[Dict]:
        """Semantic vector search"""
        query_embedding = get_embedding(query)
        
        where_filter = {"sender_type": sender_type} if sender_type else None
        
        results = self.vector_store.search(
            query_embedding=query_embedding,
            n_results=n,
            where=where_filter
        )
        
        parsed_results = []
        for id, doc, dist, meta in zip(
            results["ids"],
            results["documents"],
            results["distances"],
            results["metadatas"]
        ):
            parsed_results.append({
                "id": id,
                "text": doc,
                "score": 1.0 - dist,  # Convert distance to similarity
                "metadata": meta,
                "source": "vector"
            })
        
        return parsed_results
    
    def _keyword_search(
        self,
        query: str,
        sender_type: Optional[str],
        n: int
    ) -> List[Dict]:
        """BM25 keyword search"""
        results = self.keyword_searcher.search(
            query=query,
            top_k=n,
            filter_sender_type=sender_type
        )
        
        parsed_results = []
        for id, score, meta in results:
            # Get document text from database
            message = self.db.query(Message).filter(Message.id == id).first()
            if message:
                text = f"From: {message.sender_name}\n{message.content}"
                parsed_results.append({
                    "id": id,
                    "text": text,
                    "score": float(score) / 100.0,  # Normalize BM25 score
                    "metadata": meta,
                    "source": "keyword"
                })
        
        return parsed_results
    
    def _graph_search(
        self,
        sender_type: str,
        n: int
    ) -> List[Dict]:
        """Graph-based precedent search"""
        # Get past decisions for this sender type
        decisions = (
            self.db.query(Decision)
            .join(Message)
            .filter(Message.sender_type == sender_type)
            .order_by(Decision.timestamp.desc())
            .limit(n)
            .all()
        )
        
        parsed_results = []
        for decision in decisions:
            message = decision.message
            text = f"Previous decision: {decision.human_action}\nMessage: {message.content}"
            
            parsed_results.append({
                "id": decision.id,
                "text": text,
                "score": 0.8,  # Fixed relevance for precedent
                "metadata": {
                    "decision_id": decision.id,
                    "message_id": message.id,
                    "sender_type": sender_type,
                    "action": decision.human_action.get("action"),
                    "tone": decision.human_action.get("tone")
                },
                "source": "graph"
            })
        
        return parsed_results


def reciprocal_rank_fusion(
    rankings: List[List[str]],
    k: int = 60
) -> List[str]:
    """Combine multiple rankings using Reciprocal Rank Fusion
    
    Args:
        rankings: List of ranked item ID lists
        k: Constant for RRF formula (default 60)
        
    Returns:
        Fused ranking as list of IDs
    """
    scores = {}
    
    for ranking in rankings:
        for rank, item_id in enumerate(ranking):
            if item_id not in scores:
                scores[item_id] = 0
            scores[item_id] += 1 / (k + rank + 1)
    
    # Sort by score
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [item_id for item_id, _ in fused]

