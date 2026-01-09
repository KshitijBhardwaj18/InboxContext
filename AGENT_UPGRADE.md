# Intelligent Agent Upgrade

## Overview

The agent has been completely rewritten from basic heuristics to **sophisticated LLM-powered reasoning** with deep context understanding.

## What Changed

### ❌ Before (Basic Agent)

- Hardcoded if/else logic for sender types
- Simple vote counting for precedent
- No message understanding
- Generic reasoning
- No context awareness

```python
# Old logic
if sender_type == "investor":
    return "reply_now", "neutral"
elif sender_type == "support":
    return "reply_now", "warm"
# ...more hardcoded rules
```

### ✅ After (Intelligent Agent)

- **LLM-powered intent analysis**: Understands what the sender wants
- **Hybrid retrieval**: Combines vector, keyword, and graph search
- **Contextual reasoning**: Makes decisions based on full context
- **Sophisticated prompts**: Guides LLM to make nuanced decisions
- **Draft generation**: Creates contextual email responses
- **Graceful fallbacks**: Works without LLM if unavailable

```python
# New pipeline
1. Analyze message (intent, topics, urgency)
2. Retrieve relevant context (hybrid search)
3. LLM makes decision with reasoning
4. Generate contextual draft
5. Return comprehensive suggestion
```

## Key Features

### 1. Deep Message Analysis

The agent now **understands** messages, not just matches keywords:

```python
{
  "intent": "urgent_request",
  "topics": ["Q4", "metrics", "meeting"],
  "urgency": "high",
  "requires_action": true
}
```

**Supported Intents:**

- `question`, `information_request`, `meeting_request`
- `urgent_request`, `complaint`, `feedback`
- `sales_pitch`, `partnership_proposal`, `investment_inquiry`
- `support_request`, `follow_up`, `introduction`, `casual_check_in`

### 2. Hybrid Context Retrieval

Combines multiple search strategies:

```python
# Semantic: "Q4 metrics" matches "quarterly performance"
# Keyword: "Q4" exactly matches past messages
# Graph: Past investor decisions
# Rerank: Cross-encoder scores relevance
```

### 3. LLM-Powered Reasoning

The agent makes intelligent decisions by considering:

- ✅ Message intent and urgency
- ✅ Sender importance and past relationship
- ✅ Similar past decisions (precedents)
- ✅ Retrieved context and patterns
- ✅ Explicit and implicit signals

**Example Reasoning:**

```
"Based on 5 past investor messages, you consistently reply warmly
and promptly. The follow-up nature suggests this is part of an
ongoing conversation requiring timely response. The mention of
'metrics' indicates a business-critical topic."
```

### 4. Contextual Draft Generation

Generates email drafts that:

- Match the requested tone (warm, neutral, formal)
- Reference past context
- Address the sender's main points
- Include clear next steps
- Sound natural and human-like

### 5. Graceful Fallbacks

The system has multiple fallback layers:

```
1. LLM-powered reasoning (best)
   ↓ (if LLM unavailable)
2. Precedent voting (good)
   ↓ (if no precedents)
3. Heuristics (acceptable)
```

## API Changes

### Agent Response Schema

**New fields added:**

```python
{
  "action": "reply_now",
  "tone": "warm",
  "reasoning": "Detailed reasoning...",
  "precedent_count": 5,
  "similar_decisions": ["dec_1", "dec_2"],
  "draft_response": "Hi there! Thanks for...",  # LLM-generated

  # NEW FIELDS:
  "message_analysis": {
    "intent": "urgent_request",
    "topics": ["Q4", "metrics"],
    "urgency": "high",
    "requires_action": true
  },
  "context_sources": ["semantic_vector", "keyword_bm25", "graph"]
}
```

### Endpoint Update

```python
POST /agent/suggest/{message_id}?use_llm=true

# Query params:
# - use_llm: bool = True (use LLM or fallback to heuristics)
```

## Performance Characteristics

| Feature              | Time       | Quality       |
| -------------------- | ---------- | ------------- |
| Message Analysis     | ~500ms     | High          |
| Hybrid Retrieval     | ~200ms     | Very High     |
| LLM Reasoning        | ~1-2s      | Excellent     |
| Draft Generation     | ~1-2s      | Excellent     |
| **Total (with LLM)** | **~3-4s**  | **Excellent** |
| **Total (fallback)** | **~300ms** | **Good**      |

## Configuration

### Enable/Disable LLM

```python
# In code
agent = AgentEngine(db, use_llm=True)

# Via API
GET /agent/suggest/{msg_id}?use_llm=false
```

### LLM Settings

Edit `backend/llm.py`:

```python
class LLMClient:
    def __init__(self, model: str = "llama3.2:3b"):
        # Change model here
        # Options: llama3.2:3b, llama3:8b, etc.
```

### Prompt Tuning

Edit `backend/prompts.py`:

- `DEFAULT_SYSTEM_PROMPT`: Agent's persona
- `TONE_DESCRIPTIONS`: How each tone is interpreted
- `build_intent_analysis_prompt()`: Intent extraction
- `build_email_draft_prompt()`: Draft generation

## Testing

### Test the Intelligent Agent

```bash
# Inside Docker
docker-compose exec backend python test_advanced_agent.py

# Or locally
cd backend
source venv/bin/activate
python test_advanced_agent.py
```

### Test Without LLM (Fallback Mode)

```bash
python test_advanced_agent.py --no-llm
```

### Manual API Testing

```bash
# Get suggestion with LLM
curl http://localhost:8000/agent/suggest/msg_123

# Get suggestion without LLM (fast fallback)
curl http://localhost:8000/agent/suggest/msg_123?use_llm=false
```

## Examples

### Example 1: Urgent Investor Request

**Input:**

```
From: Sarah Chen (investor)
Subject: Q4 Metrics - Need ASAP
Content: Can we hop on a call today? Need to discuss Q4 performance before board meeting.
```

**Agent Output:**

```json
{
  "action": "reply_now",
  "tone": "neutral",
  "reasoning": "This is a time-sensitive investor request with explicit urgency ('ASAP', 'today'). Based on 3 past investor interactions, you prioritize prompt, professional responses. The board meeting context suggests high stakes requiring immediate attention.",
  "message_analysis": {
    "intent": "urgent_request",
    "topics": ["Q4", "metrics", "call", "board meeting"],
    "urgency": "critical",
    "requires_action": true
  },
  "draft_response": "Hi Sarah, absolutely. I'm available at 2pm or 4pm today. I'll send over the Q4 dashboard right now so you can review before the call. Let me know which time works.",
  "precedent_count": 3,
  "context_sources": ["semantic_vector", "graph"]
}
```

### Example 2: Sales Pitch (Should Ignore)

**Input:**

```
From: marketing@saastool.com (sales)
Subject: 10X Your Productivity!
Content: Join our exclusive webinar to learn how top companies use our tool to boost efficiency!
```

**Agent Output:**

```json
{
  "action": "ignore",
  "tone": "neutral",
  "reasoning": "This is a promotional sales pitch with typical marketing language ('10X', 'exclusive', 'boost'). Based on past decisions, you consistently ignore unsolicited sales emails and webinar invitations. No response needed.",
  "message_analysis": {
    "intent": "sales_pitch",
    "topics": ["webinar", "productivity", "tool"],
    "urgency": "low",
    "requires_action": false
  },
  "draft_response": null,
  "precedent_count": 7,
  "context_sources": ["keyword_bm25", "semantic_vector"]
}
```

### Example 3: Support Request (Warm Tone)

**Input:**

```
From: Alex Johnson (support)
Subject: Help with API integration
Content: I'm stuck on the authentication flow. The docs mention OAuth but I'm getting 401 errors. Any guidance?
```

**Agent Output:**

```json
{
  "action": "reply_now",
  "tone": "warm",
  "reasoning": "This is a technical support request from a user facing a blocking issue. Your past support interactions show a pattern of responding warmly and helpfully. The specific technical nature ('401 errors') requires a detailed, friendly response.",
  "message_analysis": {
    "intent": "support_request",
    "topics": ["API", "authentication", "OAuth", "errors"],
    "urgency": "medium",
    "requires_action": true
  },
  "draft_response": "Hey Alex! Sorry you're hitting that issue. The 401 usually means the OAuth token isn't being passed correctly. Can you share your request headers? In the meantime, check out this example: [link]. Happy to hop on a quick call if that helps!",
  "precedent_count": 5,
  "context_sources": ["semantic_vector", "keyword_bm25", "graph"]
}
```

## Best Practices

### 1. Build Precedent First

- Make 5-10 decisions before expecting good suggestions
- Vary sender types to teach different patterns
- Override when agent is wrong to correct behavior

### 2. Monitor Reasoning

- Read the reasoning field to understand decisions
- Check if it references relevant precedents
- Verify context sources are appropriate

### 3. Tune Prompts

- Adjust `DEFAULT_SYSTEM_PROMPT` for your domain
- Add domain-specific intents to `build_intent_analysis_prompt()`
- Customize `TONE_DESCRIPTIONS` for your communication style

### 4. Performance Optimization

- Use `use_llm=false` for quick previews
- Cache LLM client (already done)
- Limit `top_k` in retrieval for faster responses

## Troubleshooting

### "LLM unavailable" Error

**Cause:** Ollama not running or model not pulled

**Fix:**

```bash
# Start Ollama
ollama serve

# Pull model
ollama pull llama3.2:3b

# Restart backend
docker-compose restart backend
```

### Agent Returns Generic Suggestions

**Cause:** No precedent yet or LLM disabled

**Fix:**

1. Make at least 5 decisions to build precedent
2. Ensure `use_llm=true` in API calls
3. Check Ollama is running: `curl http://localhost:11434`

### Slow Response Times

**Cause:** LLM generation takes time

**Options:**

1. Use smaller model: `llama3.2:3b` (faster)
2. Disable draft generation if not needed
3. Use `use_llm=false` for instant suggestions

### Poor Quality Reasoning

**Cause:** Insufficient context or bad prompts

**Fix:**

1. Review and tune `backend/prompts.py`
2. Increase `top_k` in retrieval
3. Add more detailed precedents
4. Try larger model: `llama3:8b`

## Future Enhancements

Possible improvements:

1. **User Profile Learning**: Adapt to individual writing style
2. **Multi-turn Conversations**: Track email threads
3. **Calendar Integration**: Consider schedule when suggesting times
4. **Sentiment Analysis**: Detect emotional tone in messages
5. **Auto-categorization**: Tag messages by type
6. **Priority Scoring**: Rank inbox by importance
7. **Smart Scheduling**: Suggest optimal reply times

## Conclusion

The upgraded agent is now **truly intelligent**, not just rule-based. It:

✅ Understands message intent and urgency  
✅ Retrieves relevant context effectively  
✅ Makes sophisticated, reasoned decisions  
✅ Generates natural, contextual drafts  
✅ Learns from every decision  
✅ Explains its reasoning clearly

This brings the system much closer to a **production-ready AI inbox assistant** that could genuinely impress technical recruiters and founders.
