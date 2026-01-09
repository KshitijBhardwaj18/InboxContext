# Architecture Documentation

## System Overview

The Inbox Context Graph is a full-stack demonstration of a context-aware AI agent system that learns from human decisions to improve future suggestions.

## Core Concept

**Problem**: AI agents make suggestions in isolation without learning from human feedback.

**Solution**: Capture every human decision as a "decision trace," store it in a graph, and use precedent to inform future suggestions.

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                   │
│  ┌─────────┐  ┌──────────┐  ┌─────────────────┐   │
│  │ Inbox   │  │  Graph   │  │ Decision History│   │
│  │   UI    │  │ Viewer   │  │                 │   │
│  └─────────┘  └──────────┘  └─────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────────────────┐
│              Backend (FastAPI)                       │
│  ┌────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Agent    │  │   Hybrid     │  │  Decision  │ │
│  │  Engine    │  │  Retrieval   │  │  Capture   │ │
│  └────────────┘  └──────────────┘  └────────────┘ │
└──────────────────┬──────────────────────────────────┘
                   │ SQL + Embeddings
┌──────────────────▼──────────────────────────────────┐
│              PostgreSQL Database                     │
│  ┌─────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │Messages │  │Decisions │  │  Graph Nodes     │  │
│  │         │  │          │  │  & Edges         │  │
│  └─────────┘  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Data Model

### Core Entities

#### 1. Message
Represents an inbox message.

```python
{
    "id": str,
    "sender_name": str,
    "sender_type": "investor" | "sales" | "support",
    "channel": "email" | "slack" | "discord",
    "subject": str,
    "content": str,
    "timestamp": datetime,
    "embedding": [float]  # 1536-dim vector
}
```

#### 2. Decision (Canonical Object)
The heart of the system. Captures what the agent suggested vs what the human chose.

```python
{
    "decision_id": str,
    "message_id": str,
    "agent_suggestion": {
        "action": "reply_now" | "reply_later" | "ignore",
        "tone": "neutral" | "warm" | "formal"
    },
    "human_action": {
        "action": str,
        "tone": str
    },
    "context_used": {
        "sender_type": str,
        "similar_decisions": [str]  # IDs of precedent decisions
    },
    "why": str,  # Reasoning
    "timestamp": datetime
}
```

#### 3. Graph Nodes & Edges
For visualization. Represents the context graph structure.

**Node Types:**
- `message`: A message node
- `decision`: A decision node
- `sender_type`: Sender type category (investor, sales, support)
- `action`: Action chosen (reply_now, reply_later, ignore)
- `tone`: Tone chosen (neutral, warm, formal)

**Edge Types:**
- `has_decision`: Message → Decision
- `chose_action`: Decision → Action
- `chose_tone`: Decision → Tone
- `from_sender_type`: Decision → SenderType
- `based_on_precedent`: Decision → PrecedentDecision

## Agent Logic

### Base Logic (No Precedent)
Simple heuristics based on sender type:

```python
if sender_type == "investor":
    return "reply_now", "neutral"
elif sender_type == "support":
    return "reply_now", "warm"
elif sender_type == "sales":
    if is_spam(content):
        return "ignore", "neutral"
    return "reply_later", "formal"
```

### Precedent-Aware Logic
When similar decisions exist:

1. **Hybrid Retrieval**: Find similar past decisions
   - Semantic similarity (embeddings)
   - Filtered by sender_type
   
2. **Pattern Extraction**: Count human actions from precedent
   ```python
   action_counts = {"reply_now": 3, "reply_later": 1}
   tone_counts = {"warm": 4}
   ```

3. **Apply Majority**: Use most common action/tone
   ```python
   suggested_action = "reply_now"  # appeared 3 times
   suggested_tone = "warm"  # appeared 4 times
   ```

4. **Explain**: Build reasoning string
   ```
   "Based on 4 prior investor message(s), you usually chose 
   'reply_now' with 'warm' tone. Applying that precedent."
   ```

## Hybrid Retrieval

Combines two retrieval strategies:

### 1. Semantic Similarity
- Embed message content using OpenAI `text-embedding-3-small`
- Calculate cosine similarity with past messages
- Find semantically similar contexts

### 2. Structured Filtering
- Filter by `sender_type` (investor, sales, support)
- Ensures precedent is contextually relevant
- Prevents cross-contamination between categories

### Algorithm
```python
def hybrid_retrieval(message, limit=5):
    # Get embedding
    embedding = get_embedding(message.content)
    
    # Find decisions with same sender_type
    candidates = db.query(Decision).join(Message).filter(
        Message.sender_type == message.sender_type
    ).all()
    
    # Calculate similarity scores
    similarities = [
        (decision, cosine_similarity(embedding, decision.message.embedding))
        for decision in candidates
    ]
    
    # Return top matches
    return sorted(similarities, key=lambda x: x[1], reverse=True)[:limit]
```

## Frontend Components

### 1. MessageList
- Displays inbox messages
- Shows sender type badges
- Click to select

### 2. MessageDetail
- Shows selected message
- Triggers agent suggestion
- Allows accept/override
- Captures decision

### 3. GraphViewer
- React Flow visualization
- Color-coded node types
- Clickable nodes for details
- Precedent edges highlighted

### 4. DecisionHistory
- Timeline of all decisions
- Highlights overrides
- Shows precedent usage

## API Endpoints

### Messages
- `GET /messages` - List all messages
- `GET /messages/{id}` - Get single message

### Agent
- `POST /agent/suggest/{message_id}` - Get AI suggestion
  - Returns: action, tone, reasoning, precedent_count

### Decisions
- `POST /decisions` - Capture decision trace
- `GET /decisions` - List all decisions

### Graph
- `GET /graph` - Get graph nodes and edges

### Demo
- `POST /reset` - Reset all decisions (keeps messages)

## Key Flows

### Flow 1: First Decision (No Precedent)
1. User clicks message
2. Frontend calls `POST /agent/suggest/{id}`
3. Agent runs base logic
4. Returns suggestion with "No precedent found"
5. User accepts/overrides
6. Frontend calls `POST /decisions`
7. Backend stores decision + updates graph

### Flow 2: Nth Decision (With Precedent)
1. User clicks message
2. Frontend calls `POST /agent/suggest/{id}`
3. Agent runs hybrid retrieval
4. Finds 3 similar past decisions
5. Extracts pattern: "warm tone used 3/3 times"
6. Returns precedent-aware suggestion
7. User accepts (validating the learning!)
8. Decision captured with precedent links

### Flow 3: Graph Visualization
1. User clicks "Context Graph" tab
2. Frontend calls `GET /graph`
3. Backend queries graph_nodes and graph_edges
4. Frontend renders with React Flow
5. User clicks decision node
6. Shows decision trace details

## Design Decisions

### Why PostgreSQL instead of Neo4j?
- Lower barrier to entry for demo
- Sufficient for MVP graph operations
- Can migrate to Neo4j if needed
- Tables + edge tables = graph-enough

### Why Decision Trace as Canonical Object?
- Makes the "why" explicit
- Captures both agent and human perspectives
- Enables counterfactual analysis
- Self-documenting system behavior

### Why Hybrid Retrieval?
- Semantic similarity alone can be too broad
- Structured filtering adds context-awareness
- Best of both worlds: meaning + structure

### Why Not Fine-tuning?
- Fine-tuning is slow and expensive
- Retrieval-based learning is instant
- Easier to inspect and debug
- More controllable behavior

## Future Extensions

### 1. Multi-user Support
Track different users' preferences separately.

### 2. Temporal Patterns
"You usually reply to investors faster on Mondays."

### 3. Relationship Tracking
"This is your 5th message from Sarah Chen. You've always been warm."

### 4. Active Learning
"I'm uncertain here. Want to provide guidance?"

### 5. Explanation Improvement
Use LLM to generate better reasoning strings.

### 6. Real Integrations
Connect to Gmail, Slack, Discord APIs.

## Performance Considerations

### Embeddings
- Cached in database (computed once per message)
- Uses OpenAI API (can switch to local models)
- 1536 dimensions (text-embedding-3-small)

### Retrieval Speed
- O(n) similarity calculation (acceptable for demo)
- Can optimize with vector DB (Pinecone, Weaviate, pgvector)
- Filtered by sender_type reduces search space

### Graph Rendering
- React Flow handles positioning
- Simple circular layout algorithm
- Could improve with force-directed layout

## Testing the System

### Test Case 1: Learning Warm Tone for Investors
1. Reset demo
2. Process 3 investor messages
3. Override to "warm" each time
4. Process 4th investor message
5. Verify agent suggests "warm"

### Test Case 2: Different Types Learn Independently
1. Train: investor → warm
2. Train: sales → formal
3. Process investor message → suggests warm
4. Process sales message → suggests formal

### Test Case 3: Graph Grows
1. Start with 0 decisions
2. Make 5 decisions
3. Graph should have:
   - 5 decision nodes
   - 5 message nodes
   - 3 action nodes (at most)
   - 3 tone nodes (at most)
   - 3 sender_type nodes (at most)
   - Precedent edges between decisions

## Conclusion

This architecture demonstrates a working context-aware agent system. It's demo-quality but real—no smoke and mirrors. Every component works together to show how capturing human decisions in a structured way can create genuinely smarter AI agents.

The key insight: **Context isn't just data; it's decisions + reasoning + precedent, all connected in a graph.**

