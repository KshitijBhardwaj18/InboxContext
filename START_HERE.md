# 🚀 START HERE

Welcome to the **Inbox Context Graph** project!

This is your entry point. Follow this guide to get up and running quickly.

---

## What is This?

A **full-stack AI agent system** that:
- 🤖 Suggests actions for inbox messages
- 👤 Learns from your decisions
- 📊 Builds a context graph of your patterns
- 🎯 Improves suggestions over time using precedent

**Demo-quality but real.** Everything works end-to-end.

---

## 🎬 Quick Demo (2 minutes)

Want to see it in action first? Watch this flow:

1. **Inbox**: Messages from investors, sales, support
2. **Click message**: AI suggests "reply_now + neutral"
3. **Override**: Change to "reply_now + warm"
4. **Repeat 3x**: Always choose "warm" for investors
5. **5th message**: AI now suggests "warm" automatically!
6. **Graph**: See your decisions forming a network
7. **Reset**: Start fresh and demo again

**The AI learned from you!** That's the magic. ✨

---

## 🏃 Quick Start (5 minutes)

### Prerequisites
```bash
# Check you have these:
python3 --version  # Need 3.9+
node --version     # Need 18+
psql --version     # Need PostgreSQL 14+
```

### Option A: Docker (Easiest)
```bash
docker-compose up -d
docker-compose exec backend python init_db.py
open http://localhost:5173
```

### Option B: Manual
```bash
# 1. Database
createdb inbox_context_graph

# 2. Backend (in one terminal)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph" > .env
python init_db.py
uvicorn main:app --reload

# 3. Frontend (in another terminal)
cd frontend
npm install
npm run dev

# 4. Open browser
open http://localhost:5173
```

**Done!** 🎉

---

## 📖 Next Steps

### New Users
1. ✅ You're here (START_HERE.md)
2. 👉 [GETTING_STARTED.md](GETTING_STARTED.md) - First-run walkthrough
3. 👉 [DEMO_GUIDE.md](DEMO_GUIDE.md) - How to demo the learning

### Developers
1. 👉 [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
2. 👉 [API_REFERENCE.md](API_REFERENCE.md) - API docs
3. 👉 [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Flow diagrams

### Quick Reference
- **Setup issues?** → [QUICKSTART.md](QUICKSTART.md)
- **API questions?** → [API_REFERENCE.md](API_REFERENCE.md)
- **Can't find something?** → [INDEX.md](INDEX.md)

---

## 🎯 What You'll See

### Tab 1: Inbox
- List of 10 messages (left)
- Click any message (right panel)
- AI suggestion appears
- Accept or override
- Confirm decision

### Tab 2: Context Graph
- Visual network of decisions
- Color-coded nodes
- Clickable for details
- See precedent connections

### Tab 3: Decision History
- Timeline of all decisions
- ✅ Accepted vs ✏️ Overridden
- Precedent counts
- Full reasoning

---

## 💡 Key Concepts (30 seconds)

**Decision Trace**: Every choice you make is captured with context
```json
{
  "agent_suggestion": {"action": "reply_now", "tone": "neutral"},
  "human_action": {"action": "reply_now", "tone": "warm"},
  "why": "Based on 4 prior investor messages..."
}
```

**Hybrid Retrieval**: Semantic similarity + structured filtering
- Find messages with similar content (AI embeddings)
- Filter by sender type (investor/sales/support)
- Return top matches as precedent

**Precedent-Aware**: Agent learns from patterns
- First decision: "No precedent found"
- Fifth decision: "Based on 4 prior messages, you usually..."

**Context Graph**: Decisions form a queryable network
- Nodes: Messages, Decisions, Actions, Tones
- Edges: Relationships and precedent links

---

## 🎮 Try This Now

**30-second test:**

1. Open http://localhost:5173
2. Click "Sarah Chen" (investor)
3. See agent suggest: "reply_now + neutral"
4. Override to: "reply_now + warm"
5. Click "Confirm Decision"
6. Click "Jessica Wong" (also investor)
7. Repeat: override to "warm"
8. Do this 2 more times for investors
9. Click 5th investor message
10. **See**: Agent now suggests "warm" automatically!

**You just taught the AI your preference!** 🎉

---

## 📁 Project Structure

```
Inbox_Context_Graph/
├── backend/          # Python FastAPI
├── frontend/         # React + Tailwind
├── *.md             # Documentation (11 files)
└── docker-compose.yml
```

**Key files:**
- `backend/agent.py` - Learning logic
- `backend/main.py` - API endpoints
- `frontend/src/App.jsx` - Main UI

---

## 🔧 Customization

Want to modify it?

**Change agent logic:**
→ Edit `backend/agent.py` - `_base_logic()` method

**Add UI features:**
→ Edit `frontend/src/components/`

**Change mock data:**
→ Edit `backend/mock_data.py`

**Modify database:**
→ Edit `backend/models.py`

---

## ❓ Troubleshooting

### Backend won't start?
```bash
# Check port 8000
lsof -i :8000
# If in use, kill it or use different port
```

### Frontend won't start?
```bash
# Delete and reinstall
rm -rf node_modules
npm install
```

### Database errors?
```bash
# Check PostgreSQL is running
pg_isready
# If not, start it
brew services start postgresql@14  # macOS
```

### Still stuck?
→ [QUICKSTART.md](QUICKSTART.md) has detailed troubleshooting

---

## 🧪 Test It Works

```bash
cd backend
python test_api.py
```

Should see: **✅ ALL TESTS PASSED!**

---

## 📚 All Documentation

1. **[README.md](README.md)** - Project overview
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** - First run
3. **[QUICKSTART.md](QUICKSTART.md)** - Setup guide
4. **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - Demo script
5. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical design
6. **[SYSTEM_FLOW.md](SYSTEM_FLOW.md)** - Flow diagrams
7. **[API_REFERENCE.md](API_REFERENCE.md)** - API docs
8. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Feature list
9. **[CHECKLIST.md](CHECKLIST.md)** - Verification
10. **[PROJECT_TREE.md](PROJECT_TREE.md)** - File structure
11. **[INDEX.md](INDEX.md)** - Doc index

---

## 🎓 Learning Path

**Beginner** (15 min):
1. Run quick start above
2. Read [GETTING_STARTED.md](GETTING_STARTED.md)
3. Try [DEMO_GUIDE.md](DEMO_GUIDE.md)

**Intermediate** (30 min):
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Review `backend/agent.py`
3. Review `frontend/src/components/MessageDetail.jsx`

**Advanced** (1 hour):
1. Read all docs
2. Explore entire codebase
3. Run tests and experiments
4. Modify and extend

---

## 🌟 Key Features

✅ **Real AI learning** - Not faked, actually learns  
✅ **Hybrid retrieval** - Semantic + structured  
✅ **Graph storage** - PostgreSQL with graph schema  
✅ **Interactive viz** - React Flow graph  
✅ **Full-stack** - React + FastAPI + PostgreSQL  
✅ **Docker ready** - One command deployment  
✅ **Well documented** - 11 doc files  
✅ **Production quality code** - Clean, typed, tested  

---

## 🚀 Ready?

**Your next action:**

1. ✅ Make sure prerequisites are installed
2. ✅ Run the quick start above
3. ✅ Open http://localhost:5173
4. ✅ Click a message and make a decision
5. ✅ Read [GETTING_STARTED.md](GETTING_STARTED.md) for the full walkthrough

---

## 💬 Questions?

- **How does it work?** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **How do I demo it?** → [DEMO_GUIDE.md](DEMO_GUIDE.md)
- **API details?** → [API_REFERENCE.md](API_REFERENCE.md)
- **Can't find something?** → [INDEX.md](INDEX.md)

---

## 🎉 You're Ready!

This is a complete, working AI agent system that learns from human decisions.

**Go build something amazing!** 🚀

---

**Quick links:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Next: [GETTING_STARTED.md](GETTING_STARTED.md)

