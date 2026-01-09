"""Intelligent agent with LLM-powered reasoning and precedent awareness"""
from sqlalchemy.orm import Session
from models import Message, Decision
from embeddings import get_embedding, cosine_similarity
from retriever import HybridRetriever
from llm import get_llm_client
from prompts import (
    build_email_draft_prompt, 
    build_intent_analysis_prompt,
    get_tone_description,
    get_sender_context
)
from typing import List, Tuple, Optional, Dict
import json


class AgentEngine:
    """Sophisticated agent that uses LLM reasoning + hybrid retrieval + precedent learning"""
    
    def __init__(self, db: Session, use_llm: bool = True):
        self.db = db
        self.retriever = HybridRetriever(db)
        self.use_llm = use_llm
        if use_llm:
            try:
                self.llm = get_llm_client()
                print("✅ AgentEngine initialized with LLM")
            except Exception as e:
                print(f"⚠️  LLM unavailable, falling back to heuristics: {e}")
                self.use_llm = False
        else:
            print("⚠️  AgentEngine initialized without LLM (heuristics only)") 
    
    def get_suggestion(self, message: Message) -> dict:
        """Generate intelligent action/tone suggestion with deep context understanding"""
        
        # Step 1: Analyze message intent and extract key information
        message_analysis = self._analyze_message(message)
        
        # Step 2: Retrieve relevant context using hybrid strategy
        retrieved_context = self._retrieve_context(message, message_analysis)
        
        # Step 3: Get past decisions for this sender type
        similar_decisions = self._get_similar_decisions(message, retrieved_context)
        
        # Step 4: Make intelligent decision using LLM reasoning
        if self.use_llm and similar_decisions:
            action, tone, reasoning = self._llm_based_suggestion(
                message, message_analysis, similar_decisions, retrieved_context
            )
        elif similar_decisions:
            # Fallback: Use precedent voting
            action, tone, reasoning = self._precedent_voting(
                similar_decisions, message.sender_type
            )
        else:
            # Fallback: Use basic heuristics
            action, tone, reasoning = self._fallback_heuristics(message, message_analysis)
        
        # Step 5: Generate draft response if LLM is available
        draft_response = None
        if self.use_llm:
            draft_response = self._generate_draft(
                message, message_analysis, retrieved_context, tone
            )
        
        result = {
            "action": action,
            "tone": tone,
            "reasoning": reasoning,
            "precedent_count": len(similar_decisions),
            "similar_decisions": [d.id for d in similar_decisions],
            "message_analysis": message_analysis,
            "context_sources": [r.get("source") for r in retrieved_context[:3]]
        }
        
        if draft_response:
            result["draft_response"] = draft_response
        
        return result
    
    def _analyze_message(self, message: Message) -> Dict:
        """Deeply analyze message to extract intent, urgency, topics, and sentiment"""
        
        if not self.use_llm:
            return {
                "intent": "unknown",
                "topics": ["general"],
                "urgency": "medium",
                "requires_action": False
            }
        
        try:
            analysis_prompt = build_intent_analysis_prompt(message.content)
            response = self.llm.generate(
                prompt=analysis_prompt,
                temperature=0.3,  # Lower temp for more consistent analysis
                max_tokens=200
            )
            
            # Parse LLM response
            analysis = {}
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == "intent":
                        analysis["intent"] = value
                    elif key == "topics":
                        analysis["topics"] = [t.strip() for t in value.split(',')]
                    elif key == "urgency":
                        analysis["urgency"] = value
                    elif key == "action":
                        analysis["requires_action"] = "yes" in value.lower()
                        analysis["action_description"] = value
            
            return analysis
            
        except Exception as e:
            print(f"Message analysis error: {e}")
            return {
                "intent": "general_inquiry",
                "topics": ["general"],
                "urgency": "medium",
                "requires_action": True
            }
    
    def _retrieve_context(self, message: Message, analysis: Dict) -> List[Dict]:
        """Retrieve relevant context using hybrid retrieval"""
        
        # Build rich query combining message content and analyzed topics
        query_parts = [message.content]
        if analysis.get("topics"):
            query_parts.extend(analysis["topics"])
        
        query = " ".join(query_parts)
        
        try:
            results = self.retriever.retrieve(
                query=query,
                sender_type=message.sender_type,
                top_k=10,
                use_vector=True,
                use_keyword=True,
                use_graph=True,
                rerank=True
            )
            return results
        except Exception as e:
            print(f"Context retrieval error: {e}")
            return []
    
    def _get_similar_decisions(
        self, 
        message: Message, 
        retrieved_context: List[Dict]
    ) -> List[Decision]:
        """Extract Decision objects from retrieved context"""
        
        decision_ids = set()
        for result in retrieved_context:
            if result.get("source") in ["graph", "precedent"]:
                dec_id = result.get("metadata", {}).get("decision_id")
                if dec_id:
                    decision_ids.add(dec_id)
        
        if not decision_ids:
            return []
        
        decisions = (
            self.db.query(Decision)
            .filter(Decision.id.in_(decision_ids))
            .limit(5)
            .all()
        )
        
        return decisions
    
    def _llm_based_suggestion(
        self,
        message: Message,
        analysis: Dict,
        similar_decisions: List[Decision],
        retrieved_context: List[Dict]
    ) -> Tuple[str, str, str]:
        """Use LLM to make sophisticated decision based on all available context"""
        
        # Build comprehensive context for LLM
        precedent_summary = self._format_precedents(similar_decisions)
        context_summary = self._format_context(retrieved_context[:5])
        sender_context = get_sender_context(message.sender_type)
        
        prompt = f"""You are an intelligent inbox assistant analyzing a message to suggest the best action.

### Message Details:
From: {message.sender_name} ({message.sender_type})
Subject: {message.subject or 'N/A'}
Content: {message.content}

### Message Analysis:
- Intent: {analysis.get('intent', 'unknown')}
- Topics: {', '.join(analysis.get('topics', ['general']))}
- Urgency: {analysis.get('urgency', 'medium')}
- Requires Action: {analysis.get('requires_action', False)}

### Sender Context:
{sender_context}

### Past Decisions (Your Precedents):
{precedent_summary}

### Related Context:
{context_summary}

### Your Task:
Based on ALL the above information, suggest:
1. **Action**: Choose from [reply_now, reply_later, ignore]
2. **Tone**: Choose from [warm, neutral, formal]
3. **Reasoning**: Explain your decision in 2-3 sentences, referencing specific precedents and context.

Consider:
- The sender's importance and your past interactions
- The message's urgency and complexity
- Patterns in your previous decisions
- The specific intent and topics of this message

Format your response as:
Action: [your choice]
Tone: [your choice]
Reasoning: [your detailed reasoning]"""

        try:
            response = self.llm.generate(
                prompt=prompt,
                temperature=0.5,  # Balanced creativity
                max_tokens=300
            )
            
            # Parse LLM response
            action = "reply_later"
            tone = "neutral"
            reasoning = "Analysis pending"
            
            for line in response.split('\n'):
                if line.startswith("Action:"):
                    suggested_action = line.split(':', 1)[1].strip().lower()
                    if suggested_action in ["reply_now", "reply_later", "ignore"]:
                        action = suggested_action
                elif line.startswith("Tone:"):
                    suggested_tone = line.split(':', 1)[1].strip().lower()
                    if suggested_tone in ["warm", "neutral", "formal"]:
                        tone = suggested_tone
                elif line.startswith("Reasoning:"):
                    reasoning = line.split(':', 1)[1].strip()
            
            return action, tone, reasoning
            
        except Exception as e:
            print(f"LLM suggestion error: {e}")
            return self._precedent_voting(similar_decisions, message.sender_type)
    
    def _format_precedents(self, decisions: List[Decision]) -> str:
        """Format past decisions for LLM context"""
        if not decisions:
            return "No past decisions found for this type of message."
        
        formatted = []
        for i, dec in enumerate(decisions[:5], 1):
            msg = dec.message
            formatted.append(
                f"{i}. Message from {msg.sender_name} ({msg.sender_type}): "
                f'"{msg.content[:80]}..." → '
                f"You chose: {dec.human_action['action']} with {dec.human_action['tone']} tone"
            )
        
        return "\n".join(formatted)
    
    def _format_context(self, context_results: List[Dict]) -> str:
        """Format retrieved context for LLM"""
        if not context_results:
            return "No additional context retrieved."
        
        formatted = []
        for i, ctx in enumerate(context_results[:5], 1):
            source = ctx.get("source", "unknown")
            content = ctx.get("content", "")[:100]
            formatted.append(f"{i}. [{source}] {content}...")
        
        return "\n".join(formatted)
    
    def _precedent_voting(
        self,
        similar_decisions: List[Decision],
        sender_type: str
    ) -> Tuple[str, str, str]:
        """Fallback: Vote based on precedent patterns"""
        
        action_counts = {}
        tone_counts = {}
        
        for decision in similar_decisions:
            human_action = decision.human_action["action"]
            human_tone = decision.human_action["tone"]
            
            action_counts[human_action] = action_counts.get(human_action, 0) + 1
            tone_counts[human_tone] = tone_counts.get(human_tone, 0) + 1
        
        most_common_action = max(action_counts, key=action_counts.get)
        most_common_tone = max(tone_counts, key=tone_counts.get)
        
        n = len(similar_decisions)
        reasoning = (
            f"Based on {n} similar {sender_type} message(s), "
            f"you typically chose '{most_common_action}' with '{most_common_tone}' tone."
        )
        
        return most_common_action, most_common_tone, reasoning
    
    def _fallback_heuristics(
        self, 
        message: Message, 
        analysis: Dict
    ) -> Tuple[str, str, str]:
        """Basic heuristics when no precedent exists"""
        
        urgency = analysis.get("urgency", "medium")
        intent = analysis.get("intent", "unknown")
        sender_type = message.sender_type
        
        # Urgency-based logic
        if urgency in ["high", "critical"]:
            action = "reply_now"
            tone = "neutral"
            reasoning = f"High urgency {intent} from {sender_type} requires immediate attention."
        
        # Intent-based logic
        elif intent in ["urgent_request", "question"]:
            action = "reply_now"
            tone = "warm"
            reasoning = f"Direct question or request from {sender_type} needs prompt response."
        
        elif intent in ["sales_pitch", "newsletter"]:
            action = "ignore"
            tone = "neutral"
            reasoning = "Promotional content - no response needed."
        
        # Sender-based logic
        elif sender_type == "investor":
            action = "reply_now"
            tone = "neutral"
            reasoning = "Investor communications are high priority and require timely response."
        
        elif sender_type == "support":
            action = "reply_now"
            tone = "warm"
            reasoning = "Customer support requests should be handled warmly and promptly."
        
        else:
            action = "reply_later"
            tone = "neutral"
            reasoning = f"Standard {sender_type} communication can be addressed when convenient."
        
        return action, tone, reasoning
    
    def _generate_draft(
        self,
        message: Message,
        analysis: Dict,
        retrieved_context: List[Dict],
        tone: str
    ) -> Optional[str]:
        """Generate intelligent email draft using full context"""
        try:
            # Build prompt with rich context
            system_prompt, user_prompt = build_email_draft_prompt(
                message_content=message.content,
                sender_name=message.sender_name,
                sender_type=message.sender_type,
                retrieved_context=retrieved_context[:3],
                tone=tone
            )
            
            # Add analysis context to prompt
            enhanced_prompt = f"""{user_prompt}

### Additional Context:
- Message Intent: {analysis.get('intent', 'general')}
- Key Topics: {', '.join(analysis.get('topics', ['general']))}
- Urgency: {analysis.get('urgency', 'medium')}

Write a {get_tone_description(tone)} response that addresses the main points naturally."""
            
            # Generate draft
            draft = self.llm.generate(
                prompt=enhanced_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            return draft.strip()
            
        except Exception as e:
            print(f"Draft generation error: {e}")
            return None