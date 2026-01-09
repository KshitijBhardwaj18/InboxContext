# Quick Start Guide

## 🚀 Fastest Setup (3 Commands)

```bash
# 1. Install Ollama (if not installed)
brew install ollama  # macOS
# OR
curl -fsSL https://ollama.ai/install.sh | sh  # Linux

# 2. Run the automated setup script
./setup_local_models.sh

# 3. Done! Visit http://localhost:5173
```

## 📋 What Gets Installed

| Component | Purpose | Size | Auto-Downloads |
|-----------|---------|------|----------------|
| **Ollama + Llama3.2:3b** | Local LLM for text generation | ~2 GB | Yes |
| **all-MiniLM-L6-v2** | Sentence embeddings | ~90 MB | Yes (on first use) |
| **ChromaDB** | Vector database | ~20 MB | Yes |
| **BM25 + Reranker** | Keyword search + reranking | ~100 MB | Yes |

## ⚡ Manual Setup (If Script Fails)

### Step 1: Install Ollama
```bash
# Check if installed
ollama --version

# If not, install
brew install ollama  # macOS
```

### Step 2: Start Ollama & Pull Model
```bash
# Terminal 1: Start Ollama service
ollama serve

# Terminal 2: Pull the model
ollama pull llama3.2:3b

# Verify
ollama list
```

### Step 3: Start Docker Services
```bash
# From project root
docker-compose up --build

# Initialize database (in new terminal)
docker-compose exec backend python init_db.py
```

## 🔍 Verify Everything Works

### Check Ollama
```bash
curl http://localhost:11434/api/tags
# Should see llama3.2:3b in the list
```

### Check Backend
```bash
curl http://localhost:8000/messages
# Should return array of messages
```

### Check Vector Store
```bash
docker-compose exec backend python -c "import chromadb; print('ChromaDB OK')"
```

### Check Embeddings
```bash
docker-compose exec backend python -c "from sentence_transformers import SentenceTransformer; print('Sentence-Transformers OK')"
```

## 🐛 Troubleshooting

### "Ollama not found"
```bash
# Install it first
brew install ollama  # macOS
curl -fsSL https://ollama.ai/install.sh | sh  # Linux
```

### "Connection refused to Ollama"
```bash
# Start the service
ollama serve
# Keep this terminal open
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.2:3b

# See all available models
ollama list
```

### "ChromaDB directory not found"
```bash
# Initialize the database
docker-compose exec backend python init_db.py
```

### "Sentence-transformer download slow"
```bash
# Just wait, it's ~90MB
# Or pre-download:
docker-compose exec backend python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## 📊 System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB | 8 GB+ |
| Disk Space | 5 GB | 10 GB+ |
| CPU | 2 cores | 4+ cores |
| GPU | Not required | Optional (faster) |

## 🎯 Usage

1. **Open frontend**: http://localhost:5173
2. **Click a message**: See AI suggestions
3. **View draft**: LLM-generated response
4. **Accept/Override**: Make your decision
5. **View graph**: See decision patterns

## 📦 What's Running

```bash
# Check all services
docker-compose ps

# Expected output:
# NAME                    STATUS    PORTS
# postgres                Up        5432
# backend                 Up        8000
# frontend                Up        5173
```

## 🔄 Restart Everything

```bash
# Full reset
docker-compose down
docker-compose up --build
docker-compose exec backend python init_db.py
```

## 📚 More Info

- Full guide: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Architecture: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)
- Main docs: [README.md](README.md)

## 💡 Pro Tips

1. **Keep Ollama running**: Start `ollama serve` in a separate terminal
2. **Use smaller model**: `llama3.2:3b` is faster than `llama3:8b`
3. **Check logs**: `docker-compose logs -f backend`
4. **Reset vector DB**: Delete `backend/chroma_db/` and re-run `init_db.py`

---

**Questions?** Check the full [SETUP_GUIDE.md](SETUP_GUIDE.md)

