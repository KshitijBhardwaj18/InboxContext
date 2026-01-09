# Testing the Intelligent Agent

## Prerequisites

1. **Ollama installed and running:**

   ```bash
   ollama serve
   ```

2. **Model pulled:**

   ```bash
   ollama pull llama3.2:3b
   ```

3. **Services running:**

   ```bash
   docker-compose up
   ```

4. **Database initialized:**
   ```bash
   docker-compose exec backend python init_db.py
   ```

## Quick Test

### 1. Test Agent Intelligence

```bash
docker-compose exec backend python test_advanced_agent.py
```

**What to expect:**

- ✅ Deep message analysis (intent, topics, urgency)
- ✅ Intelligent reasoning with precedent references
- ✅ Contextual email drafts
- ✅ Multiple context sources (vector, keyword, graph)

### 2. Test via API

```bash
# Get all messages
curl http://localhost:8000/messages

# Pick a message ID and get suggestion
curl http://localhost:8000/agent/suggest/msg_001

# Get suggestion without LLM (fast)
curl "http://localhost:8000/agent/suggest/msg_001?use_llm=false"
```

### 3. Test via Frontend

1. Open http://localhost:5173
2. Click any message
3. See intelligent suggestion with:
   - Action and tone
   - Detailed reasoning
   - AI-generated draft
   - Context sources

## Detailed Testing Scenarios

### Scenario 1: Urgent Investor Message

**Test:** Create an urgent investor message

```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "sender_name": "Emily Wang",
    "sender_type": "investor",
    "channel": "email",
    "subject": "URGENT: Q4 Numbers",
    "content": "Can we hop on a call TODAY? Board meeting tomorrow and I need the latest Q4 metrics ASAP."
  }'
```

**Expected Agent Behavior:**

- Action: `reply_now`
- Urgency: `critical` or `high`
- Reasoning: References urgency, board meeting context
- Draft: Offers specific times, promises to send materials

### Scenario 2: Casual Sales Pitch

```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "sender_name": "growth@saastool.io",
    "sender_type": "sales",
    "channel": "email",
    "subject": "Boost Your Productivity 10X!",
    "content": "Join our exclusive webinar next week to learn how top companies use our amazing tool!"
  }'
```

**Expected Agent Behavior:**

- Action: `ignore`
- Intent: `sales_pitch`
- Reasoning: Identifies promotional language, references past pattern
- Draft: `null` (no response needed)

### Scenario 3: Support Request

```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "sender_name": "John Doe",
    "sender_type": "support",
    "channel": "email",
    "subject": "Help with API",
    "content": "I'm getting 401 errors when trying to authenticate. The docs mention OAuth but it's not working. Can you help?"
  }'
```

**Expected Agent Behavior:**

- Action: `reply_now`
- Tone: `warm`
- Intent: `support_request`
- Topics: Contains "API", "OAuth", "authentication"
- Draft: Helpful, specific, friendly response

### Scenario 4: Build Precedent

**Goal:** Teach the agent your preferences

1. Make 5 decisions with investor messages → choose `warm` tone
2. On the 6th investor message:
   - Agent should suggest `warm` tone
   - Reasoning should reference past 5 decisions
   - This proves **precedent learning works**

```bash
# Example flow
for i in {1..5}; do
  # Create investor message
  curl -X POST http://localhost:8000/messages -H "Content-Type: application/json" \
    -d "{\"sender_name\":\"Investor $i\",\"sender_type\":\"investor\",\"content\":\"Question about our progress\"}"

  # Get suggestion
  MSG_ID=$(curl http://localhost:8000/messages | jq -r ".[-1].id")

  # Make decision (override to warm)
  curl -X POST http://localhost:8000/decisions -H "Content-Type: application/json" \
    -d "{
      \"message_id\":\"$MSG_ID\",
      \"agent_suggestion\":{\"action\":\"reply_now\",\"tone\":\"neutral\"},
      \"human_action\":{\"action\":\"reply_now\",\"tone\":\"warm\"}
    }"
done
```

## Validation Checklist

### ✅ Agent Intelligence

- [ ] Message analysis extracts correct intent
- [ ] Topics are relevant to message content
- [ ] Urgency level matches message tone
- [ ] Reasoning references specific precedents
- [ ] Multiple context sources are used

### ✅ Draft Quality

- [ ] Draft addresses the sender's question/request
- [ ] Tone matches suggestion (warm/neutral/formal)
- [ ] Natural language, not robotic
- [ ] Includes clear next step
- [ ] Appropriate length (~50-100 words)

### ✅ Precedent Learning

- [ ] After 3+ similar decisions, agent learns pattern
- [ ] Reasoning explicitly mentions precedent count
- [ ] Suggestions align with past human choices
- [ ] Similar sender types get consistent treatment

### ✅ Performance

- [ ] Response time < 5 seconds with LLM
- [ ] Response time < 500ms without LLM
- [ ] No crashes or errors in logs
- [ ] Graceful fallback when Ollama unavailable

### ✅ Context Retrieval

- [ ] Vector search finds semantically similar messages
- [ ] Keyword search catches exact matches
- [ ] Graph search returns related decisions
- [ ] Reranking improves relevance

## Debugging

### Check Logs

```bash
# Backend logs
docker-compose logs -f backend

# Look for:
# ✅ "Connected to Ollama"
# ✅ "AgentEngine initialized with LLM"
# ❌ "LLM unavailable" (means Ollama not running)
```

### Verify Ollama

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Should return list of models including llama3.2:3b
```

### Test Components Individually

```bash
# Test embeddings
docker-compose exec backend python -c "from embeddings import get_embedding; print(len(get_embedding('test')))"

# Test vector store
docker-compose exec backend python test_vector_store.py

# Test retriever
docker-compose exec backend python -c "from retriever import HybridRetriever; from database import SessionLocal; db = SessionLocal(); r = HybridRetriever(db); print('OK')"

# Test LLM
docker-compose exec backend python -c "from llm import get_llm_client; llm = get_llm_client(); print(llm.generate('Say hi', max_tokens=10))"
```

### Common Issues

**Issue:** "Ollama connection failed"

```bash
# Fix: Start Ollama
ollama serve

# Or if using Docker, ensure host.docker.internal is accessible
```

**Issue:** "No precedent found"

```bash
# Fix: Make some decisions first
# The agent needs at least 1-2 past decisions to learn from
```

**Issue:** "LLM response parsing failed"

```bash
# Fix: Check prompts.py - ensure format instructions are clear
# Or use fallback: ?use_llm=false
```

## Performance Benchmarks

Target performance (tested on M1 Mac, 16GB RAM):

| Operation            | Target Time | Actual (Your System) |
| -------------------- | ----------- | -------------------- |
| Message Analysis     | < 500ms     | **\_\_\_**           |
| Hybrid Retrieval     | < 300ms     | **\_\_\_**           |
| LLM Reasoning        | < 2s        | **\_\_\_**           |
| Draft Generation     | < 2s        | **\_\_\_**           |
| **Total (with LLM)** | **< 4s**    | ****\_\_\_****       |
| **Total (no LLM)**   | **< 500ms** | ****\_\_\_****       |

Run benchmark:

```bash
time curl http://localhost:8000/agent/suggest/msg_001
```

## Success Criteria

Your agent is working well if:

1. ✅ **Reasoning is specific**, not generic

   - Good: "Based on 3 past investor messages where you replied warmly..."
   - Bad: "This is an investor message."

2. ✅ **Drafts are contextual**, not templated

   - Good: "Thanks for the Q4 question! I can send the dashboard now..."
   - Bad: "Thank you for your message. I will get back to you."

3. ✅ **Learning is visible**

   - After 5 decisions, suggestions should match your pattern
   - Reasoning should reference specific precedent count

4. ✅ **Retrieval is relevant**

   - Context sources should make sense for the query
   - Similar messages should be retrieved

5. ✅ **Performance is acceptable**
   - < 5 seconds for full LLM-powered response
   - < 500ms for fallback suggestions

## Next Steps

Once testing passes:

1. **Demo to others:** Show before/after learning
2. **Tune prompts:** Adjust `prompts.py` for your domain
3. **Add more messages:** Build a richer dataset
4. **Deploy:** Consider hosting on AWS/GCP
5. **Extend:** Add more intents, sender types, actions

---

**Questions?** Check [AGENT_UPGRADE.md](AGENT_UPGRADE.md) for detailed documentation.
