# Project Summary: Inbox Context Graph

## What Was Built

A **complete, working full-stack application** that demonstrates how AI agents can learn from human decisions through a context graph architecture.

## ✅ All MVP Requirements Met

### 1. Mock Inbox UI ✅
- React-based message list
- Displays 10 mock messages (investors, sales, support)
- Shows sender name, type, channel, timestamp
- Click to trigger agent run
- No real APIs (as specified)

### 2. Agent Suggestion Engine ✅
- FastAPI backend with deterministic logic
- Proposes: action (reply_now/reply_later/ignore) + tone (neutral/warm/formal)
- Uses message content + sender type + retrieved precedent
- Simple but deterministic logic

### 3. Human Override Capture ✅
- UI allows accept OR override
- Clear action/tone selectors
- Visual indication of override vs acceptance
- Confirmation step before capture

### 4. Decision Trace ✅
**Exact schema implemented:**
```json
{
  "decision_id": "uuid",
  "message_id": "msg_id",
  "agent_suggestion": {"action": "reply_now", "tone": "neutral"},
  "human_action": {"action": "reply_now", "tone": "warm"},
  "context_used": {
    "sender_type": "investor",
    "similar_decisions": ["dec_12", "dec_19"]
  },
  "why": "Investor relationship precedent",
  "timestamp": "ISO8601"
}
```
This object is the center of the system (as required).

### 5. Context Graph Persistence ✅
**PostgreSQL with graph-style schema:**

**Nodes:**
- Message
- Decision  
- SenderType
- Action
- Tone

**Edges:**
- MESSAGE → DECISION
- DECISION → ACTION
- DECISION → TONE
- DECISION → SENDER_TYPE
- DECISION → PRECEDENT_DECISION

Fully queryable as a graph (via SQL joins).

### 6. Hybrid Retrieval Layer ✅
**Implemented:**
- Semantic similarity via OpenAI embeddings (cosine similarity)
- Structured filtering by sender_type
- Retrieves similar past decisions
- Feeds precedent into agent suggestions

Works with or without OpenAI API key (mock embeddings fallback).

### 7. Precedent-Aware Agent Behavior ✅
**Visible behavior change:**
- First few decisions: "No precedent found. Using default logic..."
- After 3-5 decisions: "Based on 4 prior investor messages, you usually chose 'warm' tone"
- Agent explicitly references precedent count
- Suggestions improve based on human patterns

**This requirement is critical and fully demonstrated.**

### 8. Context Graph Viewer ✅
**React Flow visualization:**
- Shows all nodes and edges
- Color-coded by type
- Clickable decision nodes
- Displays decision trace details (the "why")
- Precedent edges highlighted in red with animation

### 9. Before vs After Demonstration ✅
**"Reset Demo" button:**
- Clears all decisions (keeps messages)
- Start fresh demo
- 1-2 decisions → generic behavior
- 5-6 decisions → improved, precedent-aware behavior

**Contrast is visible and compelling.**

## Tech Stack (As Requested)

✅ **Frontend**: React + Tailwind CSS  
✅ **Backend**: Python FastAPI  
✅ **Database**: PostgreSQL (graph-style schema)  
✅ **Embeddings**: OpenAI API (with mock fallback)  
✅ **Graph Viz**: React Flow  

## Project Structure

```
Inbox_Context_Graph/
├── backend/
│   ├── main.py              # FastAPI app with all endpoints
│   ├── models.py            # SQLAlchemy models (graph schema)
│   ├── schemas.py           # Pydantic schemas
│   ├── agent.py             # Agent engine with precedent logic
│   ├── embeddings.py        # Embedding service + similarity
│   ├── database.py          # DB connection
│   ├── config.py            # Settings
│   ├── mock_data.py         # 10 inbox messages
│   ├── init_db.py           # Database initialization
│   ├── test_api.py          # API test script
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker image
│   └── env.template         # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app (tabs, state)
│   │   ├── main.jsx         # React entry point
│   │   ├── index.css        # Tailwind imports
│   │   ├── api.js           # API client
│   │   ├── utils.js         # Utilities
│   │   └── components/
│   │       ├── MessageList.jsx       # Inbox UI
│   │       ├── MessageDetail.jsx     # Message + suggestion + override
│   │       ├── GraphViewer.jsx       # React Flow graph
│   │       └── DecisionHistory.jsx   # Decision timeline
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite config
│   ├── tailwind.config.js   # Tailwind config
│   ├── postcss.config.js    # PostCSS config
│   ├── index.html           # HTML entry
│   └── Dockerfile           # Docker image
│
├── docker-compose.yml       # Full stack deployment
├── setup.sh                 # Setup script
├── README.md                # Main documentation
├── QUICKSTART.md            # Setup guide
├── DEMO_GUIDE.md            # Demo walkthrough
├── ARCHITECTURE.md          # Technical deep dive
├── PROJECT_SUMMARY.md       # This file
└── .gitignore               # Git ignore rules
```

## Key Files

### Backend Core
- `main.py` - API endpoints, graph update logic
- `agent.py` - Suggestion engine, hybrid retrieval, precedent application
- `models.py` - Database schema with graph structure
- `embeddings.py` - Semantic similarity computation

### Frontend Core  
- `App.jsx` - Main component with tabs and state management
- `MessageDetail.jsx` - Critical: shows suggestion + override UI
- `GraphViewer.jsx` - React Flow visualization
- `api.js` - HTTP client for backend

## API Endpoints

```
GET  /messages              - List inbox messages
GET  /messages/{id}         - Get single message
POST /agent/suggest/{id}    - Get AI suggestion
POST /decisions             - Capture decision trace
GET  /decisions             - List all decisions
GET  /graph                 - Get graph (nodes + edges)
POST /reset                 - Reset demo
```

## Database Schema

```sql
-- Core tables
messages (id, sender_name, sender_type, channel, content, embedding, timestamp)
decisions (id, message_id, agent_suggestion, human_action, context_used, why, timestamp)
decision_precedents (id, decision_id, precedent_id)  -- Edge table

-- Graph visualization
graph_nodes (id, node_type, label, properties)
graph_edges (id, source_id, target_id, edge_type)
```

## How It Works

### 1. Agent Logic
```python
# Base logic (no precedent)
if sender_type == "investor":
    return "reply_now", "neutral"
    
# With precedent
similar_decisions = hybrid_retrieval(message)  # Semantic + filtered
action_counts = count_actions(similar_decisions)
most_common_action = max(action_counts)
return most_common_action, reasoning
```

### 2. Hybrid Retrieval
```python
# Get embedding
embedding = openai.embeddings.create(text)

# Filter by context
candidates = db.query(Decision).filter(
    sender_type == message.sender_type
)

# Rank by similarity
similarities = [cosine_similarity(embedding, c.embedding) 
                for c in candidates]
return top_k(similarities)
```

### 3. Decision Capture
```python
# Frontend sends
decision = {
    message_id: "...",
    agent_suggestion: {action, tone},
    human_action: {action, tone},  # May differ!
    context_used: {sender_type, similar_decisions},
    why: "reasoning string"
}

# Backend stores + updates graph
db.add(Decision(**decision))
update_graph_nodes_and_edges(decision)
```

## Testing

```bash
# API tests
cd backend
python test_api.py

# Manual testing
1. Open http://localhost:5173
2. Click message → see suggestion
3. Override → confirm
4. Repeat 3-4 times
5. See precedent appear in next suggestion
6. View graph visualization
```

## What Makes This Demo-Quality But Real

**Real:**
- ✅ Actual database with real schema
- ✅ Actual embeddings (via OpenAI)
- ✅ Actual graph queries
- ✅ Actual learning behavior
- ✅ End-to-end functionality

**Demo-quality:**
- ⚠️ No authentication
- ⚠️ No error recovery
- ⚠️ Simple layout algorithm
- ⚠️ Mock message data
- ⚠️ Basic UI (but functional and modern)

This is **not a mockup**. Every feature works end-to-end.

## Demonstration Value

This project demonstrates:

1. **The Core Concept**: Context graphs for AI agents
2. **Human-in-the-Loop**: Capture + learn from decisions
3. **Visible Improvement**: Before/after behavior change
4. **Full Stack**: React + FastAPI + PostgreSQL
5. **Graph Thinking**: Decisions as connected precedent

It's a **proof of concept** that could plug into a real inbox product.

## Time to Demo

Setup: 5 minutes (with Docker)  
Demo: 10 minutes (follow DEMO_GUIDE.md)  
Total: 15 minutes to show working AI that learns from humans

## Success Metrics

✅ All 9 MVP features implemented  
✅ Full tech stack (React, FastAPI, PostgreSQL, OpenAI)  
✅ Decision trace as canonical object  
✅ Graph persistence and visualization  
✅ Hybrid retrieval working  
✅ Precedent-aware behavior visible  
✅ Before/after demo capability  
✅ Clean, modern UI  
✅ Comprehensive documentation  
✅ Docker deployment ready  

## Final Deliverables

1. **Working Application** - Full-stack, end-to-end
2. **Source Code** - Clean, documented, organized
3. **Documentation** - README, QUICKSTART, DEMO_GUIDE, ARCHITECTURE
4. **Test Script** - Automated API testing
5. **Docker Setup** - One-command deployment
6. **Demo Data** - 10 realistic inbox messages

## Next Steps (If Continuing)

**For Production:**
- Add authentication/authorization
- Real email/Slack integrations
- Production database (managed PostgreSQL)
- Vector database (Pinecone/Weaviate) for scale
- Comprehensive error handling
- Rate limiting
- Monitoring/logging

**For Demo Enhancement:**
- Better graph layout (force-directed)
- Animation when decisions are made
- Confidence scores on suggestions
- Explanation improvement with LLM
- Multi-user support
- Temporal patterns

**For Research:**
- Counterfactual analysis
- Active learning experiments
- Bias detection in decisions
- Transfer learning across users

---

**Status**: ✅ COMPLETE - All requirements met, fully functional, ready to demo.

