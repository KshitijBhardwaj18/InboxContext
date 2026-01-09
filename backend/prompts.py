"""Prompt templates for LLM generation"""
from typing import List, Dict, Optional


def build_email_draft_prompt(
    message_content: str,
    sender_name: str,
    sender_type: str,
    retrieved_context: List[Dict],
    user_preferences: Optional[Dict] = None,
    tone: str = "warm"
) -> tuple[str, str]:
    """Build prompt for email draft generation
    
    Args:
        message_content: Incoming message text
        sender_name: Name of sender
        sender_type: Type of sender (investor, sales, support)
        retrieved_context: List of relevant past interactions
        user_preferences: User's writing style preferences
        tone: Desired tone
        
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    
    # Build system prompt
    system_prompt = """You are an AI email assistant helping draft professional replies.

Guidelines:
- Keep responses concise (under 100 words)
- Be natural and conversational
- Match the requested tone
- Reference past context when relevant
- End with a clear next step or call-to-action"""
    
    # Build context section
    context_str = ""
    if retrieved_context:
        context_str = "\n### Past Context:\n"
        for i, ctx in enumerate(retrieved_context[:3], 1):
            source = ctx.get("source", "unknown")
            text = ctx.get("text", "")[:200]
            context_str += f"{i}. [{source}] {text}...\n"
    
    # Build style preferences
    style_str = ""
    if user_preferences:
        formality = user_preferences.get("formality_level", "medium")
        length = user_preferences.get("avg_response_length", 50)
        emoji = user_preferences.get("emoji_usage", False)
        
        style_str = f"\n### Your Writing Style:\n"
        style_str += f"- Formality: {formality}\n"
        style_str += f"- Typical length: ~{length} words\n"
        style_str += f"- Emoji usage: {'Yes' if emoji else 'No'}\n"
    
    # Build user prompt
    user_prompt = f"""### Incoming Message:
From: {sender_name} ({sender_type})
Message: {message_content}
{context_str}
{style_str}
### Task:
Write a {tone} reply to {sender_name}. Consider the past context and maintain your natural writing style.

Draft:"""
    
    return system_prompt, user_prompt


def build_intent_analysis_prompt(
    message_content: str
) -> str:
    """Build prompt for message intent analysis"""
    
    return f"""Analyze this message and extract key information:

Message:
{message_content}

Provide:
1. Primary Intent (e.g., question, request, update, urgent_request, casual_check_in, sales_pitch)
2. Key Topics (comma-separated keywords)
3. Urgency Level (low, medium, high, critical)
4. Action Required (yes/no and what action)

Format your response as:
Intent: [intent]
Topics: [topics]
Urgency: [level]
Action: [yes/no - description]"""


def build_precedent_summary_prompt(
    decisions: List[Dict],
    sender_type: str
) -> str:
    """Build prompt to summarize precedent patterns"""
    
    decisions_str = ""
    for i, dec in enumerate(decisions, 1):
        decisions_str += f"{i}. Action: {dec.get('action')}, Tone: {dec.get('tone')}\n"
    
    return f"""Analyze these past decisions for {sender_type} messages:

{decisions_str}

Summarize the pattern in one sentence:
Pattern:"""


def build_style_learning_prompt(
    ai_drafts: List[str],
    human_edits: List[str]
) -> str:
    """Build prompt to learn user's editing patterns"""
    
    examples = ""
    for i, (ai, human) in enumerate(zip(ai_drafts[:3], human_edits[:3]), 1):
        examples += f"\nExample {i}:"
        examples += f"\nAI wrote: {ai[:100]}..."
        examples += f"\nUser changed to: {human[:100]}..."
    
    return f"""Analyze how the user edits AI-generated drafts:
{examples}

Identify the user's preferences:
1. Length preference (shorter/longer)
2. Tone adjustment (more casual/formal)
3. Common additions (greetings, sign-offs, emojis)
4. Common removals (fluff, formalities)

Summary:"""


def build_decision_explanation_prompt(
    message: str,
    agent_suggestion: Dict,
    user_choice: Dict,
    context: List[Dict]
) -> str:
    """Build prompt to explain why a decision was made"""
    
    context_str = "\n".join([f"- {c.get('text', '')[:100]}" for c in context[:2]])
    
    return f"""Message: {message[:150]}...

Agent suggested: {agent_suggestion}
User chose: {user_choice}

Context used:
{context_str}

Explain in one sentence why the user might have overridden the suggestion:
Reason:"""


# Prompt constants
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant for inbox management.
Be concise, professional, and context-aware."""

TONE_DESCRIPTIONS = {
    "warm": "friendly, enthusiastic, personal",
    "neutral": "professional, balanced, straightforward",
    "formal": "respectful, traditional, structured"
}

SENDER_TYPE_CONTEXT = {
    "investor": "Important stakeholder requiring timely, informative responses",
    "sales": "Business inquiry requiring professional evaluation",
    "support": "User needing helpful assistance and guidance"
}


def get_tone_description(tone: str) -> str:
    """Get description of tone"""
    return TONE_DESCRIPTIONS.get(tone, "professional")


def get_sender_context(sender_type: str) -> str:
    """Get context about sender type"""
    return SENDER_TYPE_CONTEXT.get(sender_type, "General contact")

