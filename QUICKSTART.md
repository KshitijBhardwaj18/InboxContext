# Quick Start Guide

Get the Inbox Context Graph running in 5 minutes.

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- OpenAI API key (optional but recommended for real embeddings)

## Step 1: Install PostgreSQL (if not installed)

**macOS (Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql
sudo systemctl start postgresql
```

## Step 2: Create Database

```bash
createdb inbox_context_graph
```

If you need to create a postgres user first:
```bash
psql postgres
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;
\q
```

## Step 3: Clone and Setup

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# OR manually:

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

## Step 4: Configure Environment

Edit `backend/.env`:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph
OPENAI_API_KEY=sk-your-key-here  # Optional: leave empty for mock embeddings
```

**Note**: The system works without an OpenAI API key (uses mock embeddings), but real embeddings provide better semantic similarity.

## Step 5: Initialize Database

```bash
cd backend
source venv/bin/activate
python init_db.py
```

You should see: `Added 10 messages to database.`

## Step 6: Start Backend

```bash
# In backend/ directory with venv activated
uvicorn main:app --reload
```

Backend will run at http://localhost:8000

## Step 7: Start Frontend

```bash
# In a new terminal
cd frontend
npm run dev
```

Frontend will run at http://localhost:5173

## Step 8: Use the App

1. Open http://localhost:5173
2. Click any message in the inbox
3. See the AI agent suggestion
4. Accept or override the suggestion
5. Click "Confirm Decision"
6. Repeat for 3-4 messages of the same sender type
7. Notice how the agent learns from your decisions!

## Troubleshooting

### Database connection error
- Check PostgreSQL is running: `pg_isready`
- Verify database exists: `psql -l | grep inbox_context_graph`
- Check DATABASE_URL in `.env`

### Port already in use
- Backend: Change port in `main.py` or run: `uvicorn main:app --port 8001`
- Frontend: Change port in `vite.config.js`

### Import errors
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### No embeddings / slow
- Add your OPENAI_API_KEY to `backend/.env`
- Or continue with mock embeddings (works fine for demo)

## Next Steps

- Read [DEMO_GUIDE.md](DEMO_GUIDE.md) for a walkthrough
- Try the "Context Graph" tab to visualize decisions
- Click "Reset Demo" to start fresh
- Build precedent for different sender types

## Architecture Overview

```
┌─────────────┐
│   React UI  │  (Inbox, Graph Viz, History)
└──────┬──────┘
       │ HTTP
┌──────▼──────┐
│  FastAPI    │  (Agent Engine, Hybrid Retrieval)
└──────┬──────┘
       │
┌──────▼──────┐
│  PostgreSQL │  (Messages, Decisions, Graph)
└─────────────┘
```

## Key Endpoints

- `GET /messages` - List all messages
- `POST /agent/suggest/{id}` - Get AI suggestion
- `POST /decisions` - Capture decision trace
- `GET /graph` - Get context graph
- `POST /reset` - Reset demo

Enjoy exploring the Inbox Context Graph! 🚀

