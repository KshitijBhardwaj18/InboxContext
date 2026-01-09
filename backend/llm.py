"""Local LLM integration using Ollama"""
import ollama
from typing import Optional, List, Dict


class LLMClient:
    """Client for local LLM via Ollama"""
    
    def __init__(self, model: str = "llama3.2:3b"):
        """Initialize LLM client
        
        Args:
            model: Ollama model name (default: llama3.2:3b)
        """
        self.model = model
        self._check_connection()
    
    def _check_connection(self):
        """Check if Ollama is running"""
        try:
            ollama.list()
            print(f"✅ Connected to Ollama (model: {self.model})")
        except Exception as e:
            print(f"⚠️  Ollama not available: {e}")
            print("   Install: curl -fsSL https://ollama.com/install.sh | sh")
            print(f"   Then run: ollama pull {self.model}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Generate text from prompt
        
        Args:
            prompt: User prompt
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._fallback_response()
    
    def generate_email_draft(
        self,
        context: str,
        recipient_name: str,
        sender_type: str,
        tone: str = "warm",
        style_notes: Optional[str] = None
    ) -> str:
        """Generate email draft based on context
        
        Args:
            context: Retrieved context about past interactions
            recipient_name: Name of recipient
            sender_type: Type of sender (investor, sales, support)
            tone: Desired tone (warm, neutral, formal)
            style_notes: Additional style preferences
            
        Returns:
            Email draft text
        """
        system_prompt = """You are an AI email assistant. Write concise, professional emails.
Keep responses under 100 words. Be natural and conversational."""
        
        user_prompt = f"""Write an email reply based on this context:

Recipient: {recipient_name} ({sender_type})
Tone: {tone}
{f'Style: {style_notes}' if style_notes else ''}

Context from past interactions:
{context}

Generate a brief, appropriate email reply:"""
        
        draft = self.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=200
        )
        
        return draft.strip()
    
    def analyze_message_intent(
        self,
        message_content: str
    ) -> Dict[str, str]:
        """Analyze what the sender wants
        
        Args:
            message_content: Message text
            
        Returns:
            Dict with intent analysis
        """
        prompt = f"""Analyze this message and extract:
1. Primary intent (question, request, update, urgent_request, casual_check_in)
2. Key topics (comma-separated)
3. Urgency level (low, medium, high)

Message:
{message_content}

Return in format:
Intent: [intent]
Topics: [topics]
Urgency: [level]"""
        
        try:
            response = self.generate(prompt, max_tokens=100)
            
            # Parse response
            intent_data = {}
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    intent_data[key.strip().lower()] = value.strip()
            
            return intent_data
            
        except Exception:
            return {
                "intent": "unknown",
                "topics": "general",
                "urgency": "medium"
            }
    
    def _fallback_response(self) -> str:
        """Fallback when LLM is unavailable"""
        return "Thank you for your message. I'll get back to you soon."
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """Multi-turn chat
        
        Args:
            messages: List of {role: str, content: str} dicts
            temperature: Sampling temperature
            
        Returns:
            Assistant response
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={'temperature': temperature}
            )
            return response['message']['content']
        except Exception as e:
            print(f"Chat error: {e}")
            return self._fallback_response()


# Global instance
_llm_client = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client singleton"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

