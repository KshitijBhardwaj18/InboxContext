# Local Dependencies Setup Guide

This guide will help you set up all the required local models and dependencies for the Inbox Context Graph project.

## Prerequisites

- Python 3.9 or higher
- Ollama (for local LLM)
- Docker and Docker Compose (if using containerized setup)

## Option 1: Docker Setup (Recommended)

The project is configured to run in Docker, which handles all Python dependencies automatically.

### Step 1: Install Ollama on Your Host Machine

Ollama needs to run on your host machine (not in Docker) for best performance:

```bash
# For macOS (using Homebrew)
brew install ollama

# Or download from https://ollama.ai/download

# For Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Start Ollama Service

```bash
# Start Ollama server (run in a separate terminal)
ollama serve
```

### Step 3: Pull the Llama3 Model

```bash
# Pull the Llama3.2 3B model (recommended for speed)
ollama pull llama3.2:3b

# Or use the full Llama3 8B model (better quality, slower)
ollama pull llama3

# Verify the model is downloaded
ollama list
```

### Step 4: Start the Docker Services

```bash
# From the project root
docker-compose up --build
```

The backend container will automatically:

- Install all Python dependencies from `requirements.txt`
- Download the `all-MiniLM-L6-v2` sentence-transformer model on first run
- Create a ChromaDB database in the `backend/chroma_db` directory

### Step 5: Initialize the Database

```bash
# In a new terminal
docker-compose exec backend python init_db.py
```

This will:

- Create mock messages
- Chunk and embed all messages
- Store embeddings in ChromaDB
- Build the initial context graph

## Option 2: Local Python Setup

If you prefer to run everything locally without Docker:

### Step 1: Create a Virtual Environment

```bash
cd /Users/kshitij/development/Inbox_Context_Graph/backend

# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### Step 2: Install Python Dependencies

```bash
# Install all requirements
pip install -r requirements.txt
```

This will install:

- **sentence-transformers** (2.3.1): Local embedding model
- **chromadb** (0.4.22): Local vector database
- **ollama** (0.1.6): Python client for Ollama
- **rank-bm25** (0.2.2): Keyword search
- And all other FastAPI, SQLAlchemy dependencies

### Step 3: Download Sentence-Transformer Model

The model will auto-download on first use, but you can pre-download it:

```python
# Run this Python script to pre-download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Step 4: Install and Configure Ollama

Same as Docker setup (Steps 1-3 above)

### Step 5: Set Up PostgreSQL

```bash
# Install PostgreSQL locally or use Docker
docker run -d \
  --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=inbox_graph \
  -p 5432:5432 \
  postgres:15
```

### Step 6: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/inbox_graph
OLLAMA_HOST=http://localhost:11434
```

### Step 7: Run the Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Initialize the Database

```bash
# In a new terminal (with venv activated)
cd backend
source venv/bin/activate
python init_db.py
```

## Verifying Your Setup

### 1. Check Ollama

```bash
# Test Ollama is working
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello!",
  "stream": false
}'
```

### 2. Check Backend Dependencies

```bash
# Inside Docker
docker-compose exec backend python -c "import sentence_transformers; import chromadb; import ollama; print('All imports successful!')"

# Or locally
python -c "import sentence_transformers; import chromadb; import ollama; print('All imports successful!')"
```

### 3. Check ChromaDB

```bash
# List ChromaDB collections
docker-compose exec backend python -c "import chromadb; client = chromadb.PersistentClient(path='./chroma_db'); print(client.list_collections())"
```

### 4. Test the Vector Store

```bash
docker-compose exec backend python backend/test_vector_store.py
```

### 5. Check API Endpoints

```bash
# Get messages
curl http://localhost:8000/messages

# Test context retrieval
curl -X POST http://localhost:8000/context/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "investor meeting", "strategies": ["semantic", "keyword"]}'
```

## Common Issues and Solutions

### Issue 1: "Ollama connection failed"

**Solution**: Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull llama3.2:3b`)

### Issue 2: "ChromaDB directory not found"

**Solution**: Run `init_db.py` to create and populate the vector database

### Issue 3: "Sentence-transformer model download slow"

**Solution**: The `all-MiniLM-L6-v2` model is ~90MB. First download may take a few minutes.

### Issue 4: "CUDA/GPU errors"

**Solution**: The setup uses CPU by default. If you have a GPU and want to use it, install `sentence-transformers[cuda]` instead.

### Issue 5: Docker volume permissions

**Solution**: The `chroma_db` directory is created inside the backend container. Make sure it has write permissions.

## Model Specifications

### Sentence-Transformer: all-MiniLM-L6-v2

- **Size**: ~90 MB
- **Embedding Dimension**: 384
- **Speed**: Fast (CPU-friendly)
- **Use Case**: General semantic similarity

### Ollama: Llama3.2:3b

- **Size**: ~2 GB
- **Parameters**: 3 billion
- **Speed**: Very fast on CPU
- **Use Case**: Text generation, drafts, reasoning

### ChromaDB

- **Type**: Local vector database
- **Storage**: File-based (persistent)
- **Location**: `backend/chroma_db/`

## Next Steps

Once everything is set up:

1. **Test the frontend**: Navigate to `http://localhost:5173`
2. **Click a message**: See agent suggestions with precedent-aware reasoning
3. **View draft responses**: Generated by the local LLM
4. **Make decisions**: Build your context graph
5. **View the graph**: Visualize decision patterns

## Performance Tips

1. **Use smaller models**: `llama3.2:3b` is faster than `llama3:8b`
2. **Limit retrieval results**: Adjust `top_k` in API calls
3. **Cache embeddings**: ChromaDB persists embeddings across restarts
4. **Use Docker volumes**: For faster container restarts

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Sentence-Transformers Guide](https://www.sbert.net/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Need help?** Check the logs:

```bash
# Backend logs
docker-compose logs backend

# Ollama logs (if running as service)
journalctl -u ollama -f
```
