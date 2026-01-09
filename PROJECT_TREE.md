# Project File Tree

Complete file structure of the Inbox Context Graph project.

```
Inbox_Context_Graph/
│
├── 📚 Documentation (10 files)
│   ├── README.md                    # Main overview and quick start
│   ├── INDEX.md                     # Documentation index
│   ├── GETTING_STARTED.md           # First-run walkthrough
│   ├── QUICKSTART.md                # Detailed setup guide
│   ├── DEMO_GUIDE.md                # Demo script and talking points
│   ├── ARCHITECTURE.md              # System design and algorithms
│   ├── SYSTEM_FLOW.md               # Visual flow diagrams
│   ├── API_REFERENCE.md             # Complete API documentation
│   ├── PROJECT_SUMMARY.md           # Feature checklist and deliverables
│   ├── CHECKLIST.md                 # Implementation verification
│   └── PROJECT_TREE.md              # This file
│
├── 🐳 Deployment (3 files)
│   ├── docker-compose.yml           # Docker orchestration
│   ├── setup.sh                     # Automated setup script
│   └── .gitignore                   # Git ignore rules
│
├── 🔧 Backend (13 files)
│   ├── main.py                      # FastAPI application
│   │   • API endpoints (7 routes)
│   │   • Graph update logic
│   │   • CORS configuration
│   │
│   ├── agent.py                     # Agent suggestion engine
│   │   • Base logic (no precedent)
│   │   • Hybrid retrieval
│   │   • Precedent application
│   │   • Reasoning generation
│   │
│   ├── models.py                    # SQLAlchemy models
│   │   • Message (inbox messages)
│   │   • Decision (decision traces)
│   │   • DecisionPrecedent (edges)
│   │   • GraphNode (visualization)
│   │   • GraphEdge (visualization)
│   │
│   ├── schemas.py                   # Pydantic schemas
│   │   • MessageBase, Message
│   │   • AgentSuggestion, HumanAction
│   │   • DecisionTrace
│   │   • GraphResponse
│   │
│   ├── embeddings.py                # Embedding service
│   │   • OpenAI API integration
│   │   • Cosine similarity
│   │   • Mock embeddings fallback
│   │
│   ├── database.py                  # Database connection
│   │   • SQLAlchemy engine
│   │   • Session management
│   │   • Connection pooling
│   │
│   ├── config.py                    # Configuration
│   │   • Environment variables
│   │   • Settings management
│   │
│   ├── mock_data.py                 # Sample data
│   │   • 10 inbox messages
│   │   • Realistic content
│   │   • Mixed sender types
│   │
│   ├── init_db.py                   # Database initialization
│   │   • Create tables
│   │   • Load mock messages
│   │   • Generate embeddings
│   │
│   ├── test_api.py                  # API tests
│   │   • Endpoint verification
│   │   • Learning behavior tests
│   │   • Integration tests
│   │
│   ├── requirements.txt             # Python dependencies
│   │   • fastapi, uvicorn
│   │   • sqlalchemy, psycopg2
│   │   • openai, numpy
│   │
│   ├── env.template                 # Environment template
│   │   • DATABASE_URL
│   │   • OPENAI_API_KEY
│   │
│   └── Dockerfile                   # Docker image
│       • Python 3.11
│       • Dependencies
│       • Auto-init on start
│
└── 🎨 Frontend (12 files)
    ├── src/
    │   ├── main.jsx                 # React entry point
    │   │   • ReactDOM.render
    │   │   • App mounting
    │   │
    │   ├── App.jsx                  # Main application
    │   │   • Tab navigation
    │   │   • State management
    │   │   • Reset functionality
    │   │   • Header with stats
    │   │
    │   ├── api.js                   # API client
    │   │   • Axios configuration
    │   │   • All API methods
    │   │   • Error handling
    │   │
    │   ├── utils.js                 # Utility functions
    │   │   • Date formatting
    │   │   • Time helpers
    │   │
    │   ├── index.css                # Global styles
    │   │   • Tailwind imports
    │   │   • Base styles
    │   │
    │   └── components/
    │       │
    │       ├── MessageList.jsx      # Inbox list component
    │       │   • Message display
    │       │   • Sender type badges
    │       │   • Channel icons
    │       │   • Selection handling
    │       │
    │       ├── MessageDetail.jsx    # Message detail + agent
    │       │   • Message content
    │       │   • Agent suggestion
    │       │   • Override controls
    │       │   • Decision capture
    │       │
    │       ├── GraphViewer.jsx      # Graph visualization
    │       │   • React Flow integration
    │       │   • Node positioning
    │       │   • Color coding
    │       │   • Click handlers
    │       │   • Detail panel
    │       │
    │       └── DecisionHistory.jsx  # Decision timeline
    │           • Decision list
    │           • Accept/override indicators
    │           • Precedent badges
    │           • Reasoning display
    │
    ├── index.html                   # HTML entry point
    ├── package.json                 # Node dependencies
    │   • react, react-dom
    │   • reactflow
    │   • axios
    │   • tailwindcss
    │
    ├── vite.config.js               # Vite configuration
    ├── tailwind.config.js           # Tailwind configuration
    ├── postcss.config.js            # PostCSS configuration
    └── Dockerfile                   # Docker image
        • Node 18
        • Dependencies
        • Dev server

Total Files: 40
├── Documentation: 10
├── Backend: 13
├── Frontend: 12
├── Config/Deploy: 5
```

## File Size Estimates

```
Backend:
├── main.py          ~400 lines
├── agent.py         ~200 lines
├── models.py        ~150 lines
├── schemas.py       ~100 lines
├── embeddings.py     ~50 lines
├── Other files      ~100 lines
└── Total:           ~1000 lines

Frontend:
├── App.jsx          ~150 lines
├── MessageDetail.jsx ~250 lines
├── GraphViewer.jsx  ~200 lines
├── MessageList.jsx  ~100 lines
├── DecisionHistory.jsx ~100 lines
├── Other files       ~50 lines
└── Total:           ~850 lines

Documentation:
└── Total:           ~3000 lines

Total Project:       ~4850 lines
```

## Key Dependencies

### Backend
```python
fastapi==0.109.0          # Web framework
uvicorn==0.27.0           # ASGI server
sqlalchemy==2.0.25        # ORM
psycopg2-binary==2.9.9    # PostgreSQL driver
pydantic==2.5.3           # Data validation
openai==1.10.0            # Embeddings API
numpy==1.26.3             # Similarity calculations
```

### Frontend
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "reactflow": "^11.10.4",    // Graph visualization
  "axios": "^1.6.5",           // HTTP client
  "tailwindcss": "^3.4.1",     // CSS framework
  "vite": "^5.0.11"            // Build tool
}
```

## Database Schema

```
messages
├── id (PK)
├── sender_name
├── sender_type
├── channel
├── subject
├── content
├── timestamp
└── embedding (JSON)

decisions
├── id (PK)
├── message_id (FK → messages)
├── agent_suggestion (JSON)
├── human_action (JSON)
├── context_used (JSON)
├── why
└── timestamp

decision_precedents
├── id (PK)
├── decision_id (FK → decisions)
└── precedent_id (FK → decisions)

graph_nodes
├── id (PK)
├── node_type
├── label
└── properties (JSON)

graph_edges
├── id (PK)
├── source_id
├── target_id
└── edge_type
```

## API Endpoints

```
GET    /                      # Health check
GET    /messages              # List messages
GET    /messages/{id}         # Get message
POST   /agent/suggest/{id}    # Get suggestion
POST   /decisions             # Capture decision
GET    /decisions             # List decisions
GET    /graph                 # Get graph data
POST   /reset                 # Reset demo
```

## Component Hierarchy

```
App
├── Header
│   ├── Title
│   ├── Stats
│   └── Reset Button
├── Tabs
│   ├── Inbox Tab
│   ├── Graph Tab
│   └── History Tab
└── Content
    ├── Inbox View
    │   ├── MessageList
    │   │   └── MessageCard × N
    │   └── MessageDetail
    │       ├── MessageContent
    │       ├── AgentSuggestion
    │       ├── OverrideControls
    │       └── ConfirmButton
    ├── Graph View
    │   ├── GraphViewer
    │   │   ├── ReactFlow
    │   │   │   ├── Node × N
    │   │   │   └── Edge × N
    │   │   └── DetailPanel
    │   └── Legend
    └── History View
        └── DecisionHistory
            └── DecisionCard × N
```

## Data Flow

```
User Action
    ↓
Frontend Component
    ↓
API Client (api.js)
    ↓
HTTP Request
    ↓
FastAPI Endpoint (main.py)
    ↓
Agent Engine (agent.py)
    ├→ Embeddings (embeddings.py)
    ├→ Database Query (models.py)
    └→ Logic Processing
    ↓
Database Update (PostgreSQL)
    ↓
Response
    ↓
Frontend Update
    ↓
UI Refresh
```

## Deployment Options

### Option 1: Docker (Recommended)
```bash
docker-compose up
# Services: postgres, backend, frontend
# Ports: 5432, 8000, 5173
```

### Option 2: Manual
```bash
# Terminal 1: PostgreSQL
createdb inbox_context_graph

# Terminal 2: Backend
cd backend
uvicorn main:app --reload

# Terminal 3: Frontend
cd frontend
npm run dev
```

## Configuration Files

```
Backend:
├── backend/.env              # Environment variables
├── backend/requirements.txt  # Python deps
└── backend/Dockerfile        # Docker image

Frontend:
├── frontend/package.json     # Node deps
├── frontend/vite.config.js   # Build config
├── frontend/tailwind.config.js # Styles config
└── frontend/Dockerfile       # Docker image

Project:
├── docker-compose.yml        # Orchestration
└── .gitignore               # Git rules
```

## Quick Links

### Documentation
- Overview: [README.md](README.md)
- Setup: [QUICKSTART.md](QUICKSTART.md)
- Demo: [DEMO_GUIDE.md](DEMO_GUIDE.md)
- API: [API_REFERENCE.md](API_REFERENCE.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

### Key Files
- Backend API: `backend/main.py`
- Agent Logic: `backend/agent.py`
- Database Schema: `backend/models.py`
- Main UI: `frontend/src/App.jsx`
- Message Detail: `frontend/src/components/MessageDetail.jsx`
- Graph Viz: `frontend/src/components/GraphViewer.jsx`

### Utilities
- Setup: `setup.sh`
- Init DB: `backend/init_db.py`
- Test API: `backend/test_api.py`

---

**Status**: ✅ Complete  
**Total Files**: 40  
**Total Lines**: ~4850  
**Ready**: Production-ready demo

