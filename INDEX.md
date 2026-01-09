# Documentation Index

Complete guide to the Inbox Context Graph project.

## 🚀 Getting Started

**New here? Start with these:**

1. **[README.md](README.md)** - Project overview, quick start, and philosophy
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Step-by-step first-run guide
3. **[QUICKSTART.md](QUICKSTART.md)** - Detailed setup instructions

## 📖 Core Documentation

### User Guides
- **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - How to demonstrate the before/after learning effect
- **[API_REFERENCE.md](API_REFERENCE.md)** - All endpoints, schemas, and examples

### Technical Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, data model, and algorithms
- **[SYSTEM_FLOW.md](SYSTEM_FLOW.md)** - Visual flow diagrams and data flows
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete feature checklist and deliverables

## 📁 Project Structure

```
Inbox_Context_Graph/
├── 📄 README.md                    # Start here
├── 📄 GETTING_STARTED.md           # First-run guide
├── 📄 QUICKSTART.md                # Setup details
├── 📄 DEMO_GUIDE.md                # Demo walkthrough
├── 📄 ARCHITECTURE.md              # Technical deep dive
├── 📄 SYSTEM_FLOW.md               # Flow diagrams
├── 📄 API_REFERENCE.md             # API docs
├── 📄 PROJECT_SUMMARY.md           # Feature checklist
├── 📄 INDEX.md                     # This file
│
├── 🐳 docker-compose.yml           # Docker setup
├── 🔧 setup.sh                     # Setup script
│
├── 📂 backend/                     # Python FastAPI
│   ├── main.py                    # API application
│   ├── models.py                  # Database models
│   ├── schemas.py                 # Pydantic schemas
│   ├── agent.py                   # Agent engine
│   ├── embeddings.py              # Semantic similarity
│   ├── database.py                # DB connection
│   ├── config.py                  # Settings
│   ├── mock_data.py               # Sample messages
│   ├── init_db.py                 # Database init
│   ├── test_api.py                # API tests
│   ├── requirements.txt           # Dependencies
│   ├── Dockerfile                 # Docker image
│   └── env.template               # Config template
│
└── 📂 frontend/                    # React app
    ├── src/
    │   ├── App.jsx                # Main component
    │   ├── api.js                 # API client
    │   ├── utils.js               # Utilities
    │   └── components/
    │       ├── MessageList.jsx    # Inbox UI
    │       ├── MessageDetail.jsx  # Message + agent
    │       ├── GraphViewer.jsx    # Graph viz
    │       └── DecisionHistory.jsx # History view
    ├── package.json               # Dependencies
    ├── vite.config.js             # Vite config
    ├── tailwind.config.js         # Tailwind config
    ├── index.html                 # HTML entry
    └── Dockerfile                 # Docker image
```

## 🎯 Documentation by Role

### For Developers

**Setting up:**
1. [QUICKSTART.md](QUICKSTART.md) - Complete setup guide
2. [GETTING_STARTED.md](GETTING_STARTED.md) - First run walkthrough

**Understanding the code:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Data flows
3. [API_REFERENCE.md](API_REFERENCE.md) - API endpoints

**Testing:**
1. Run `backend/test_api.py`
2. Follow [DEMO_GUIDE.md](DEMO_GUIDE.md)

### For Demo/Presentation

**Preparation:**
1. [GETTING_STARTED.md](GETTING_STARTED.md) - Get it running
2. [DEMO_GUIDE.md](DEMO_GUIDE.md) - Demo script

**Key talking points:**
- Decision trace as canonical object
- Hybrid retrieval (semantic + structured)
- Visible behavior change (before/after)
- Context graph visualization

**Files to show:**
- `backend/agent.py` - Agent logic
- `backend/models.py` - Graph schema
- `frontend/src/components/MessageDetail.jsx` - Override UI

### For Product/Design

**Concept:**
1. [README.md](README.md) - What it does and why
2. [DEMO_GUIDE.md](DEMO_GUIDE.md) - User experience flow

**Flows:**
1. [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Visual diagrams
2. [GETTING_STARTED.md](GETTING_STARTED.md) - First-run experience

**Features:**
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete feature list

## 📚 Documentation by Topic

### Setup & Installation
- [QUICKSTART.md](QUICKSTART.md) - Manual setup
- [GETTING_STARTED.md](GETTING_STARTED.md) - First run
- `docker-compose.yml` - Docker setup
- `setup.sh` - Automated setup

### Core Concepts
- [README.md](README.md) - Overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
- [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - How it works

### User Experience
- [GETTING_STARTED.md](GETTING_STARTED.md) - First user experience
- [DEMO_GUIDE.md](DEMO_GUIDE.md) - Demonstration guide
- Frontend components - UI implementation

### API & Integration
- [API_REFERENCE.md](API_REFERENCE.md) - All endpoints
- `backend/main.py` - API implementation
- `frontend/src/api.js` - API client

### Data & Storage
- [ARCHITECTURE.md](ARCHITECTURE.md) - Database schema
- `backend/models.py` - SQLAlchemy models
- `backend/schemas.py` - Pydantic schemas

### Agent & Learning
- [ARCHITECTURE.md](ARCHITECTURE.md) - Agent logic
- [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Learning flows
- `backend/agent.py` - Implementation

### Graph & Visualization
- [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Graph structure
- `frontend/src/components/GraphViewer.jsx` - React Flow viz
- `backend/models.py` - Graph schema

## 🔍 Finding Specific Information

### "How do I...?"

**...set it up?**
→ [QUICKSTART.md](QUICKSTART.md) or [GETTING_STARTED.md](GETTING_STARTED.md)

**...demo it?**
→ [DEMO_GUIDE.md](DEMO_GUIDE.md)

**...understand how it works?**
→ [ARCHITECTURE.md](ARCHITECTURE.md) and [SYSTEM_FLOW.md](SYSTEM_FLOW.md)

**...use the API?**
→ [API_REFERENCE.md](API_REFERENCE.md)

**...modify the agent logic?**
→ `backend/agent.py` + [ARCHITECTURE.md](ARCHITECTURE.md)

**...add a new feature?**
→ [ARCHITECTURE.md](ARCHITECTURE.md) for design patterns

**...deploy it?**
→ `docker-compose.yml` + [QUICKSTART.md](QUICKSTART.md)

### "Where is...?"

**...the decision capture?**
→ `backend/main.py` - `POST /decisions` endpoint
→ `frontend/src/components/MessageDetail.jsx` - UI

**...the learning logic?**
→ `backend/agent.py` - `AgentEngine` class

**...the hybrid retrieval?**
→ `backend/agent.py` - `_hybrid_retrieval()` method

**...the graph update?**
→ `backend/main.py` - `_update_graph()` function

**...the precedent application?**
→ `backend/agent.py` - `_apply_precedent()` method

**...the visualization?**
→ `frontend/src/components/GraphViewer.jsx`

**...the mock data?**
→ `backend/mock_data.py`

**...the database schema?**
→ `backend/models.py`

## 📊 Key Files by Importance

### Critical (Core Functionality)
1. `backend/main.py` - API endpoints
2. `backend/agent.py` - Agent logic
3. `backend/models.py` - Data schema
4. `frontend/src/components/MessageDetail.jsx` - Main UI
5. `frontend/src/components/GraphViewer.jsx` - Visualization

### Important (Supporting)
1. `backend/embeddings.py` - Semantic similarity
2. `backend/schemas.py` - API contracts
3. `frontend/src/App.jsx` - App structure
4. `frontend/src/api.js` - API client
5. `backend/init_db.py` - Data initialization

### Supporting (Infrastructure)
1. `backend/database.py` - DB connection
2. `backend/config.py` - Settings
3. `backend/mock_data.py` - Sample data
4. `frontend/src/utils.js` - Utilities
5. Various config files

## 🎓 Learning Path

### Beginner
1. Read [README.md](README.md) - Understand the concept
2. Follow [GETTING_STARTED.md](GETTING_STARTED.md) - Get it running
3. Try [DEMO_GUIDE.md](DEMO_GUIDE.md) - See it in action

### Intermediate
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) - Understand the design
2. Review [SYSTEM_FLOW.md](SYSTEM_FLOW.md) - Understand the flows
3. Explore `backend/agent.py` - See the learning logic
4. Explore `backend/main.py` - See the API

### Advanced
1. Read [API_REFERENCE.md](API_REFERENCE.md) - API details
2. Study `backend/models.py` - Database design
3. Study graph visualization - React Flow integration
4. Experiment with modifications

## 🔗 External Resources

### Technologies Used
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **React Flow**: https://reactflow.dev/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **PostgreSQL**: https://www.postgresql.org/

### Related Concepts
- **Context Windows**: AI memory and context management
- **Human-in-the-Loop Learning**: ML with human feedback
- **Graph Databases**: Neo4j, graph thinking
- **Retrieval-Augmented Generation (RAG)**: Hybrid retrieval

## 💡 Quick Reference

### URLs (Local Development)
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Key Commands
```bash
# Setup
./setup.sh                          # Automated setup
createdb inbox_context_graph        # Create database
python backend/init_db.py           # Initialize data

# Run
cd backend && uvicorn main:app --reload    # Start backend
cd frontend && npm run dev                  # Start frontend

# Test
python backend/test_api.py          # API tests

# Docker
docker-compose up                   # Start all services
docker-compose down                 # Stop all services
```

### Key Concepts
- **Decision Trace**: Canonical object capturing agent + human decisions
- **Hybrid Retrieval**: Semantic similarity + structured filtering
- **Precedent**: Past decisions used to inform future suggestions
- **Context Graph**: Network of decisions, messages, and choices

## 📝 Document Maintenance

All documentation is in Markdown and can be edited with any text editor.

**Style guide:**
- Use clear headings
- Include code examples
- Add diagrams where helpful
- Link between documents
- Keep examples up-to-date

**To update:**
1. Edit the relevant `.md` file
2. Update [INDEX.md](INDEX.md) if adding new docs
3. Test any code examples
4. Check internal links

---

**Questions?** Start with [README.md](README.md) or dive into any topic above!

