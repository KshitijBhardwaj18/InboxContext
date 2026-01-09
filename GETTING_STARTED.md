# Getting Started with Inbox Context Graph

Welcome! This guide will get you up and running in **5 minutes**.

## What You're Building

An AI agent that learns from your decisions:
- 🤖 Agent suggests actions for inbox messages
- 👤 You accept or override the suggestion  
- 📊 Agent learns from your patterns
- 🎯 Future suggestions improve based on precedent

## Prerequisites Check

Do you have these installed?

```bash
# Check versions
python3 --version  # Need 3.9+
node --version     # Need 18+
psql --version     # Need PostgreSQL 14+
```

If not, install:
- **Python**: [python.org](https://python.org)
- **Node.js**: [nodejs.org](https://nodejs.org)
- **PostgreSQL**: 
  - macOS: `brew install postgresql@14`
  - Ubuntu: `sudo apt install postgresql`

## Quick Start (Choose One)

### Option A: Docker (Easiest)

```bash
# 1. Start everything
docker-compose up -d

# 2. Wait 30 seconds for services to start

# 3. Initialize database
docker-compose exec backend python init_db.py

# 4. Open browser
open http://localhost:5173

# Done! ✅
```

### Option B: Manual Setup (5 minutes)

#### Step 1: Database Setup (1 min)

```bash
# Create database
createdb inbox_context_graph

# Verify it exists
psql -l | grep inbox_context_graph
```

**Troubleshooting**: If `createdb` fails, you may need to create a postgres user first:
```bash
psql postgres
CREATE USER postgres WITH PASSWORD 'postgres' SUPERUSER;
\q
```

#### Step 2: Backend Setup (2 min)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph
OPENAI_API_KEY=
EOF

# Initialize database with mock messages
python init_db.py
# You should see: "Added 10 messages to database."

# Start backend server
uvicorn main:app --reload
# You should see: "Application startup complete."
```

Keep this terminal open! Backend runs at http://localhost:8000

#### Step 3: Frontend Setup (2 min)

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# You should see: "Local: http://localhost:5173"
```

Keep this terminal open too!

#### Step 4: Open the App

Visit: http://localhost:5173

You should see the Inbox Context Graph interface! 🎉

## First Run Walkthrough

### 1. The Inbox Tab (Default)

You'll see:
- **Left panel**: List of 10 messages (investors, sales, support)
- **Right panel**: Empty (waiting for you to select a message)

### 2. Click Your First Message

Try clicking on **"Sarah Chen"** (an investor).

Watch what happens:
1. The message details appear
2. A spinner shows while the agent thinks
3. The agent's suggestion appears:
   ```
   🤖 Agent Suggests: reply_now • neutral
   "No precedent found. Using default logic for investor."
   ```

### 3. Make Your First Decision

Notice the suggestion is "neutral" tone. Let's override it:

1. Keep action as: **reply_now**
2. Change tone to: **warm** (because investors deserve warmth!)
3. Click **"Confirm Decision"**

You'll see: "Decision captured! The agent will learn from this."

### 4. Make 3 More Investor Decisions

Click on:
- "Jessica Wong" → override to **warm**
- "David Park" → override to **warm**  
- "Tom Baker" → override to **warm**

Notice: Each time, the agent still suggests "neutral" at first.

### 5. The Magic Happens! ✨

Click on your 5th investor message.

**Now the agent suggests: "reply_now • warm"**

Read the reasoning:
```
"Based on 4 prior investor message(s), you usually chose 
'warm' tone. Applying that precedent."
```

**The agent learned from you!** 🎉

### 6. View the Context Graph

Click the **"Context Graph"** tab at the top.

You'll see:
- Purple nodes = messages
- Blue nodes = decisions
- Yellow nodes = actions (reply_now, etc.)
- Orange nodes = tones (warm, neutral, formal)
- Green nodes = sender types (investor, sales, support)

Click on a **blue decision node** to see the full decision trace.

### 7. View Decision History

Click the **"Decision History"** tab.

You'll see all your decisions with:
- ✅ = accepted agent suggestion
- ✏️ = overrode agent suggestion
- Precedent count badge

### 8. Reset and Try Again

Click **"Reset Demo"** in the top right.

This clears all decisions (but keeps messages).

Now you can:
- Try building precedent for "support" → warm
- Try building precedent for "sales" → ignore
- See how different sender types learn independently!

## Common Questions

### "The agent isn't learning after 3 decisions?"

The agent needs decisions for **the same sender type**. 

Example:
- ✅ 3 investor decisions → learns for investors
- ❌ 1 investor + 1 sales + 1 support → not enough of any one type

### "I see 'No precedent found' even after 5 decisions?"

Check that you're clicking messages of the **same sender type** you trained on.

Example:
- Trained on: investor messages (3x)
- Clicked on: sales message
- Result: No precedent (different type)

### "Should I add an OPENAI_API_KEY?"

**Optional!** The system works fine without it (uses mock embeddings).

With a real key:
- Better semantic similarity
- More accurate precedent matching
- But it costs ~$0.0001 per message

Add it to `backend/.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

### "Can I use a different database?"

The `DATABASE_URL` in `backend/.env` can point to any PostgreSQL server:
```
# Local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph

# Remote
DATABASE_URL=postgresql://user:pass@your-server.com:5432/dbname
```

### "How do I stop the servers?"

In each terminal where a server is running:
- Press `Ctrl+C`

Or with Docker:
```bash
docker-compose down
```

## Next Steps

Now that you have it running:

1. **Read [DEMO_GUIDE.md](DEMO_GUIDE.md)**  
   Learn how to demonstrate the before/after learning effect

2. **Read [ARCHITECTURE.md](ARCHITECTURE.md)**  
   Understand how the system works under the hood

3. **Experiment!**
   - Try different override patterns
   - Build complex precedents
   - See how the graph evolves

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# If something is using it, kill it or use a different port
uvicorn main:app --reload --port 8001
```

### Frontend won't start

```bash
# Check if port 5173 is in use  
lsof -i :5173

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database connection error

```bash
# Check PostgreSQL is running
pg_isready

# If not running (macOS):
brew services start postgresql@14

# If not running (Ubuntu):
sudo systemctl start postgresql

# Verify database exists
psql -l | grep inbox_context_graph

# If not, create it
createdb inbox_context_graph
```

### "command not found: createdb"

PostgreSQL isn't in your PATH. Try:

```bash
# macOS with Homebrew
/opt/homebrew/bin/createdb inbox_context_graph

# Or add to PATH
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
```

### Import errors in Python

Make sure you activated the virtual environment:

```bash
cd backend
source venv/bin/activate  # You should see (venv) in your prompt
python init_db.py
```

### Need help?

Check these files:
- [QUICKSTART.md](QUICKSTART.md) - Detailed setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
- Backend logs - Look at the terminal running the backend
- Frontend logs - Open browser DevTools (F12) → Console

## Test Your Setup

Run the automated test:

```bash
cd backend
source venv/bin/activate
python test_api.py
```

If you see "✅ ALL TESTS PASSED!" - you're good to go!

---

**You're all set!** Start clicking messages and watch the agent learn from you. 🚀

Questions? Check the docs linked above, or dive into the code - it's well-commented!

