"""Agent suggestion engine with precedent-aware logic"""
from sqlalchemy.orm import Session
from models import Message, Decision
from embeddings import get_embedding, cosine_similarity
from retriever import HybridRetriever
from llm import get_llm_client
from prompts import build_email_draft_prompt
from typing import List, Tuple, Optional


class AgentEngine:
    """Simple but deterministic agent that learns from precedent"""
    
    def __init__(self, db: Session, use_llm: bool = False):
        self.db = db
        self.retriever = HybridRetriever(db)
        self.use_llm = use_llm
        if use_llm:
            try:
                self.llm = get_llm_client()
            except Exception as e:
                print(f"LLM unavailable, will skip draft generation: {e}")
                self.use_llm = False 
    
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
        
        # Generate draft response if LLM is available
        draft_response = None
        if self.use_llm:
            draft_response = self._generate_draft(message, similar_decisions, tone)
        
        result = {
            "action": action,
            "tone": tone,
            "reasoning": reasoning,
            "precedent_count": len(similar_decisions),
            "similar_decisions": [d.id for d in similar_decisions]
        }
        
        if draft_response:
            result["draft_response"] = draft_response
        
        return result
    
    def _generate_draft(
        self,
        message: Message,
        similar_decisions: List[Decision],
        tone: str
    ) -> Optional[str]:
        """Generate email draft using LLM"""
        try:
            # Get retrieved context
            retrieved_context = []
            for decision in similar_decisions[:3]:
                retrieved_context.append({
                    "text": f"Past message: {decision.message.content[:100]}... → Action: {decision.human_action['action']}, Tone: {decision.human_action['tone']}",
                    "source": "precedent"
                })
            
            # Build prompt
            system_prompt, user_prompt = build_email_draft_prompt(
                message_content=message.content,
                sender_name=message.sender_name,
                sender_type=message.sender_type,
                retrieved_context=retrieved_context,
                tone=tone
            )
            
            # Generate draft
            draft = self.llm.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=150
            )
            
            return draft.strip()
            
        except Exception as e:
            print(f"Draft generation error: {e}")
            return None
    
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
        """Hybrid retrieval using new multi-strategy retriever"""
        
        # Use the unified hybrid retriever
        query = f"{message.subject or ''} {message.content}"
        
        results = self.retriever.retrieve(
            query=query,
            sender_type=message.sender_type,
            top_k=limit,
            use_vector=True,
            use_keyword=True,
            use_graph=True,
            rerank=True
        )
        
        # Extract decision IDs from results
        decision_ids = []
        for result in results:
            if result["source"] == "graph":
                decision_id = result["metadata"].get("decision_id")
                if decision_id:
                    decision_ids.append(decision_id)
        
        # Get Decision objects
        if not decision_ids:
            return []
        
        decisions = (
            self.db.query(Decision)
            .filter(Decision.id.in_(decision_ids))
            .all()
        )
        
        return decisions
    
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