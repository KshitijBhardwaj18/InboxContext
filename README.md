# Inbox Context Graph

> A context layer for inbox agents that captures human decision traces and turns them into a precedent-aware context graph.

**Demo-quality, real system** demonstrating how AI agents can learn from human decisions to provide increasingly personalized suggestions.

## 🎯 What This Demonstrates

This is a full-stack prototype showing:

- ✅ **AI Agent** that proposes actions (reply/ignore) and tone (neutral/warm/formal)
- ✅ **Human-in-the-Loop** decision capture with accept/override options
- ✅ **Precedent-Aware Learning** - agent improves suggestions based on past decisions
- ✅ **Hybrid Retrieval** - semantic similarity + structured filtering
- ✅ **Context Graph** - decisions stored as queryable graph structure
- ✅ **Graph Visualization** - interactive visualization with React Flow
- ✅ **Before/After Demo** - visible behavior improvement over time

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

### 1. First Decision (No Precedent)
```
User clicks message
  ↓
Agent uses basic heuristics
  → "investor" = reply_now + neutral tone
  ↓
User overrides to "warm" tone
  ↓
Decision captured ✅
```

### 2. After 3-5 Decisions (Learning Emerges)
```
User clicks another investor message
  ↓
Agent checks for similar past decisions
  → Finds 4 prior investor messages
  → Human chose "warm" in all 4
  ↓
Agent suggests: reply_now + warm tone
  → "Based on 4 prior investor messages, 
     you usually chose 'warm' tone"
  ↓
User accepts (validates learning!) ✅
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
  "agent_suggestion": {"action": "reply_now", "tone": "neutral"},
  "human_action": {"action": "reply_now", "tone": "warm"},
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

