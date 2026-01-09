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
    
    # Build system prompt with tone-specific guidance
    tone_guidance = TONE_DESCRIPTIONS.get(tone, "professional")
    
    system_prompt = f"""You are an expert AI email assistant that drafts natural, contextually-aware replies.

Your writing style should be:
- {tone_guidance}
- Concise but complete (under 100 words)
- Natural and human-like, not robotic
- Context-aware: reference past interactions when relevant
- Action-oriented: always include a clear next step

Key principles:
1. Address the sender's main points directly
2. Use the same communication style as past successful interactions
3. Be authentic - write as the user would write
4. Avoid generic templates or overly formal language unless tone is 'formal'
5. End with a clear call-to-action or next step"""
    
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
    """Build prompt for deep message intent analysis"""
    
    return f"""Analyze this message deeply and extract ALL key information:

Message:
{message_content}

Analyze and provide:
1. Primary Intent: Choose the MOST specific from [question, information_request, meeting_request, update, urgent_request, complaint, feedback, casual_check_in, sales_pitch, partnership_proposal, investment_inquiry, support_request, follow_up, introduction]
2. Key Topics: Extract 3-5 specific keywords or phrases (comma-separated)
3. Urgency Level: Rate as [low, medium, high, critical] based on language, deadlines, and tone
4. Action Required: Specify [yes/no] and describe what specific action is needed

Be specific and precise. Consider:
- Explicit requests or questions
- Implicit urgency signals (deadlines, "asap", "urgent", etc.)
- Emotional tone and sentiment
- Business context and importance

Format your response EXACTLY as:
Intent: [your choice]
Topics: [topic1, topic2, topic3]
Urgency: [your choice]
Action: [yes/no - specific description]"""


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
DEFAULT_SYSTEM_PROMPT = """You are a highly intelligent AI inbox assistant with deep understanding of context, precedent, and human communication patterns.

Your role:
- Analyze messages holistically, considering sender importance, urgency, content, and past interactions
- Learn from precedent: recognize patterns in how the user handles different types of messages
- Make nuanced decisions that balance urgency, importance, and user preferences
- Provide clear, actionable reasoning that references specific context

Always consider:
1. The user's relationship with the sender (past interactions)
2. The message's true urgency (not just stated urgency)
3. Patterns in how the user handles similar situations
4. The broader context and implications of the message"""

TONE_DESCRIPTIONS = {
    "warm": "friendly, enthusiastic, personal, showing genuine interest and care",
    "neutral": "professional, balanced, straightforward, matter-of-fact",
    "formal": "respectful, traditional, structured, maintaining clear boundaries"
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

