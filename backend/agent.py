"""Agent suggestion engine with precedent-aware logic"""
from sqlalchemy.orm import Session
from models import Message, Decision
from embeddings import get_embedding, cosine_similarity
from typing import List, Tuple


class AgentEngine:
    """Simple but deterministic agent that learns from precedent"""
    
    def __init__(self, db: Session):
        self.db = db 
    
    def get_suggestion(self, message: Message) -> dict:
        """Generate action/tone suggestion based on message + precedent"""
        
        # Get similar past decisions via hybrid retrieval
        similar_decisions = self._hybrid_retrieval(message)
        
        # Base suggestion (before learning)
        base_action, base_tone = self._base_logic(message)
        
        # Precedent-aware adjustment
        if similar_decisions:
            action, tone, reasoning = self._apply_precedent(
                base_action, base_tone, similar_decisions, message.sender_type
            )
        else:
            action = base_action
            tone = base_tone
            reasoning = f"No precedent found. Using default logic for {message.sender_type}."
        
        return {
            "action": action,
            "tone": tone,
            "reasoning": reasoning,
            "precedent_count": len(similar_decisions),
            "similar_decisions": [d.id for d in similar_decisions]
        }
    
    def _base_logic(self, message: Message) -> Tuple[str, str]:
        """Default logic without precedent"""
        sender_type = message.sender_type
        
        # Simple heuristics
        if sender_type == "investor":
            return "reply_now", "neutral"
        elif sender_type == "support":
            return "reply_now", "warm"
        elif sender_type == "sales":
            # Check for obvious spam patterns
            content_lower = message.content.lower()
            if any(word in content_lower for word in ["webinar", "newsletter", "register now"]):
                return "ignore", "neutral"
            return "reply_later", "formal"
        else:
            return "reply_later", "neutral"
    
    def _hybrid_retrieval(self, message: Message, limit: int = 5) -> List[Decision]:
        """Hybrid retrieval: semantic + structured filtering"""
        
        # Get message embedding
        message_embedding = message.embedding
        if not message_embedding:
            # Generate if not exists
            message_embedding = get_embedding(message.content)
        
        # Get all decisions for same sender_type
        decisions = (
            self.db.query(Decision)
            .join(Message)
            .filter(Message.sender_type == message.sender_type)
            .all()
        )
        
        if not decisions:
            return []
        
        # Calculate semantic similarity
        similarities = []
        for decision in decisions:
            if decision.message.embedding:
                similarity = cosine_similarity(message_embedding, decision.message.embedding)
                similarities.append((decision, similarity))
        
        # Sort by similarity and take top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [d for d, _ in similarities[:limit]]
    
    def _apply_precedent(
        self, 
        base_action: str, 
        base_tone: str, 
        similar_decisions: List[Decision],
        sender_type: str
    ) -> Tuple[str, str, str]:
        """Apply precedent to adjust suggestion"""
        
        # Count human actions from precedent
        action_counts = {}
        tone_counts = {}
        
        for decision in similar_decisions:
            human_action = decision.human_action["action"]
            human_tone = decision.human_action["tone"]
            
            action_counts[human_action] = action_counts.get(human_action, 0) + 1
            tone_counts[human_tone] = tone_counts.get(human_tone, 0) + 1
        
        # Get most common action and tone from precedent
        most_common_action = max(action_counts, key=action_counts.get)
        most_common_tone = max(tone_counts, key=tone_counts.get)
        
        # Build reasoning
        n = len(similar_decisions)
        reasoning = (
            f"Based on {n} prior {sender_type} message(s), "
            f"you usually chose '{most_common_action}' with '{most_common_tone}' tone. "
            f"Applying that precedent."
        )
        
        return most_common_action, most_common_tone, reasoning

