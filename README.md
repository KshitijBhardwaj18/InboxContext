# Inbox Context Graph

> A production-grade RAG-powered context layer for inbox agents with hybrid retrieval, local LLM integration, and precedent-aware learning.

**Full-stack system** demonstrating advanced retrieval techniques and AI agent learning from human feedback.

## 🎯 What This Demonstrates

### Core Features

- ✅ **Intelligent Agent** - LLM-powered reasoning with deep context understanding
- ✅ **Intent Analysis** - Automatic message intent, urgency, and topic extraction
- ✅ **Multi-Modal Retrieval** - Vector (semantic) + Keyword (BM25) + Graph (precedent)
- ✅ **Local LLM Integration** - Ollama/Llama3 for reasoning and draft generation
- ✅ **Cross-Encoder Reranking** - Improve retrieval quality with re-scoring
- ✅ **Vector Database** - ChromaDB for persistent embeddings
- ✅ **Local Embeddings** - sentence-transformers (no API required)
- ✅ **Context Graph** - PostgreSQL graph schema for decision relationships
- ✅ **Precedent Learning** - Agent learns from human overrides and patterns
- ✅ **Graph Visualization** - React Flow interactive display
- ✅ **Production RAG** - Chunking, metadata filtering, hybrid fusion

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose up

# Initialize database (first time only)
docker-compose exec backend python init_db.py

# Open http://localhost:5173
```

### Option 2: Manual Setup

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

```bash
# 1. Create PostgreSQL database
createdb inbox_context_graph

# 2. Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph" > .env
python init_db.py
uvicorn main:app --reload

# 3. Setup frontend (new terminal)
cd frontend
npm install
npm run dev

# 4. Open http://localhost:5173
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
- **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - How to demonstrate the before/after learning
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep dive into system design

## 🏗️ Architecture

```
┌─────────────┐
│   React UI  │  ← Inbox, Graph Viz, Decision History
└──────┬──────┘
       │ REST API
┌──────▼──────┐
│  FastAPI    │  ← Agent Engine, Hybrid Retrieval
└──────┬──────┘
       │ SQL
┌──────▼──────┐
│ PostgreSQL  │  ← Messages, Decisions, Context Graph
└─────────────┘
```

**Tech Stack:**

- Frontend: React + Tailwind CSS + React Flow
- Backend: Python FastAPI
- Database: PostgreSQL (graph-style schema)
- Embeddings: OpenAI API (optional, works without)

## 🎮 How It Works

### Intelligent Agent Pipeline

```
User clicks message
  ↓
1️⃣ DEEP ANALYSIS (LLM)
  → Extract intent, topics, urgency
  → Identify if action required
  ↓
2️⃣ HYBRID RETRIEVAL
  → Semantic search (embeddings)
  → Keyword search (BM25)
  → Graph traversal (precedents)
  → Cross-encoder reranking
  ↓
3️⃣ LLM REASONING
  → Analyze message + context + precedents
  → Make sophisticated decision
  → Explain reasoning with references
  ↓
4️⃣ DRAFT GENERATION
  → Generate contextual email draft
  → Match tone and style
  ↓
5️⃣ PRESENT TO USER
  → Show action, tone, reasoning
  → Display draft response
  → User accepts or overrides
  ↓
6️⃣ LEARNING
  → Capture decision trace
  → Update context graph
  → Store in vector DB
```

### Example: First Message (No Precedent)

```
📧 Message from Investor: "Can we sync about Q4 metrics?"
  ↓
🔍 Analysis: urgent_request, topics: [Q4, metrics, sync]
  ↓
🤖 Agent Decision: reply_now + neutral
  Reasoning: "Urgent investment inquiry requires immediate attention"
  Draft: "Happy to sync! I'm available Tuesday or Wednesday..."
  ↓
✏️ User Override: reply_now + warm
  ↓
✅ Decision captured as precedent
```

### Example: After Learning (With Precedents)

```
📧 Another Investor Message: "Following up on our last chat..."
  ↓
🔍 Analysis: follow_up, topics: [follow_up, previous discussion]
  ↓
📚 Retrieval: Finds 5 similar investor interactions
  → User always chose "warm" tone
  → Always replied within same day
  ↓
🤖 Agent Decision: reply_now + warm
  Reasoning: "Based on 5 past investor messages, you consistently
  reply warmly and promptly. The follow-up nature suggests this
  is part of an ongoing conversation requiring timely response."
  Draft: "Thanks for following up! Here's where we are..."
  ↓
✅ User accepts (validates learned pattern!)
```

### 3. Context Graph

```
Every decision becomes nodes + edges:
  Message → Decision → Action
                    → Tone
                    → SenderType
                    → PrecedentDecisions
```

## 💡 Key Features

### Decision Trace (Canonical Object)

Every decision is captured with full context:

```json
{
  "decision_id": "uuid",
  "message_id": "msg_123",
  "agent_suggestion": { "action": "reply_now", "tone": "neutral" },
  "human_action": { "action": "reply_now", "tone": "warm" },
  "context_used": {
    "sender_type": "investor",
    "similar_decisions": ["dec_12", "dec_19"]
  },
  "why": "Based on 2 prior investor messages, you usually replied warmly",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Hybrid Retrieval

Combines two strategies:

1. **Semantic Similarity** - Find messages with similar content (embeddings)
2. **Structured Filtering** - Filter by sender_type (investor/sales/support)

Result: Context-aware precedent that actually makes sense.

### Graph Visualization

Interactive graph showing:

- Message nodes (purple)
- Decision nodes (blue)
- Action/Tone/SenderType nodes (yellow/orange/green)
- Precedent edges (red, animated)

Click any decision node to see full trace.

## 🧪 Testing

```bash
# Run API tests
cd backend
python test_api.py

# Should see:
# ✅ ALL TESTS PASSED!
```

## 🎬 Demo Flow

1. **Reset** - Click "Reset Demo" to start fresh
2. **Make 2-3 decisions** - Notice generic reasoning ("No precedent found")
3. **Make 2-3 more** - Notice precedent appearing ("Based on 3 prior messages...")
4. **View Graph** - See decisions forming a network
5. **Celebrate** - The agent learned from you! 🎉

## 📊 Use Cases

This pattern works for:

- **Email management** - Learn reply patterns per sender type
- **Customer support** - Learn escalation patterns per issue type
- **Code review** - Learn approval patterns per code smell
- **Content moderation** - Learn moderation decisions per violation type

Any domain where:

1. AI makes suggestions
2. Humans make final decisions
3. Patterns emerge over time

## 🛠️ Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload  # Auto-reload on changes
```

### Frontend Development

```bash
cd frontend
npm run dev  # Hot module replacement
```

### Database Reset

```bash
# Reset decisions only (keep messages)
curl -X POST http://localhost:8000/reset

# Full reset (including messages)
cd backend
python init_db.py
```

## 🔧 Configuration

### Environment Variables (backend/.env)

```bash
# Required
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph

# Optional (system works without it using mock embeddings)
OPENAI_API_KEY=sk-your-key-here
```

## 🎯 Design Philosophy

**Demo-quality, not production-ready:**

- Real working code, not mockups
- Visible behavior change (the key demo requirement)
- Simple but correct implementation
- Prioritize clarity over optimization

**NOT included (intentionally):**

- Authentication/authorization
- Rate limiting
- Error recovery
- Production deployment config
- Extensive test coverage
- Performance optimization

This is a **working prototype** to demonstrate the concept. It shows the core idea clearly.

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # SQLAlchemy models
│   ├── agent.py             # Agent suggestion engine
│   ├── embeddings.py        # Semantic similarity
│   ├── init_db.py           # Database initialization
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── components/
│   │   │   ├── MessageList.jsx
│   │   │   ├── MessageDetail.jsx
│   │   │   ├── GraphViewer.jsx
│   │   │   └── DecisionHistory.jsx
│   │   └── api.js           # API client
│   └── package.json
├── QUICKSTART.md            # Setup instructions
├── DEMO_GUIDE.md            # Demo walkthrough
├── ARCHITECTURE.md          # Technical deep dive
└── docker-compose.yml       # Docker setup
```

## 🤝 Contributing

This is a demonstration project. Feel free to fork and extend!

Ideas for extensions:

- Multi-user support
- Real Gmail/Slack integration
- Temporal patterns ("you reply faster on Mondays")
- Active learning ("I'm uncertain, want to guide me?")
- Better graph layout algorithms

## 📝 License

MIT - Use freely for demos, learning, or as a starting point for your own projects.

---

Built to demonstrate how **context graphs** can make AI agents genuinely smarter over time. 🚀
