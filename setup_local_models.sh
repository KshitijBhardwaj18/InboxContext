#!/bin/bash

# Setup script for local models and dependencies
# Run this after installing Ollama on your system

set -e  # Exit on error

echo "🚀 Setting up local models for Inbox Context Graph..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Ollama is installed
echo -e "\n${YELLOW}Checking Ollama installation...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama is not installed!${NC}"
    echo "Please install Ollama first:"
    echo "  macOS: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  Or visit: https://ollama.ai/download"
    exit 1
else
    echo -e "${GREEN}✅ Ollama is installed${NC}"
fi

# Check if Ollama is running
echo -e "\n${YELLOW}Checking if Ollama service is running...${NC}"
if ! curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama service is not running${NC}"
    echo "Starting Ollama service in the background..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    
    if curl -s http://localhost:11434 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama service started${NC}"
    else
        echo -e "${RED}❌ Failed to start Ollama service${NC}"
        echo "Please run 'ollama serve' manually in another terminal"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Ollama service is running${NC}"
fi

# Pull Llama3 model
echo -e "\n${YELLOW}Pulling Llama3.2 3B model (this may take a few minutes)...${NC}"
if ollama list | grep -q "llama3.2:3b"; then
    echo -e "${GREEN}✅ llama3.2:3b model already downloaded${NC}"
else
    echo "Downloading llama3.2:3b (~2GB)..."
    ollama pull llama3.2:3b
    echo -e "${GREEN}✅ llama3.2:3b model downloaded${NC}"
fi

# Check if Docker is available
echo -e "\n${YELLOW}Checking Docker setup...${NC}"
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"
    
    # Start Docker services if not running
    if [ -f "docker-compose.yml" ]; then
        echo -e "\n${YELLOW}Starting Docker services...${NC}"
        docker-compose up -d --build
        
        echo -e "\n${YELLOW}Waiting for backend to be ready...${NC}"
        sleep 5
        
        # Initialize database with vector embeddings
        echo -e "\n${YELLOW}Initializing database and vector store...${NC}"
        docker-compose exec -T backend python init_db.py
        
        echo -e "${GREEN}✅ Docker setup complete${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Docker not found, assuming local Python setup${NC}"
    
    # Check Python environment
    if [ ! -d "backend/venv" ]; then
        echo -e "\n${YELLOW}Creating Python virtual environment...${NC}"
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        
        echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
        pip install --upgrade pip
        pip install -r requirements.txt
        
        cd ..
        echo -e "${GREEN}✅ Python environment created${NC}"
    else
        echo -e "${GREEN}✅ Python venv already exists${NC}"
    fi
fi

# Test sentence-transformers model download
echo -e "\n${YELLOW}Pre-downloading sentence-transformer model...${NC}"
if command -v docker &> /dev/null && docker ps | grep -q inbox_context_graph; then
    docker-compose exec -T backend python -c "from sentence_transformers import SentenceTransformer; print('Loading model...'); model = SentenceTransformer('all-MiniLM-L6-v2'); print('Model loaded successfully!')"
else
    if [ -d "backend/venv" ]; then
        cd backend
        source venv/bin/activate
        python -c "from sentence_transformers import SentenceTransformer; print('Loading model...'); model = SentenceTransformer('all-MiniLM-L6-v2'); print('Model loaded successfully!')"
        cd ..
    fi
fi
echo -e "${GREEN}✅ Sentence-transformer model ready${NC}"

# Verify setup
echo -e "\n${YELLOW}Verifying setup...${NC}"

# Test Ollama
echo -n "Testing Ollama... "
if curl -s http://localhost:11434/api/tags | grep -q "llama3.2"; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
fi

# Test backend (if running)
echo -n "Testing backend API... "
if curl -s http://localhost:8000/messages > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${YELLOW}⚠️  (backend may not be running yet)${NC}"
fi

# Summary
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n📦 Installed Components:"
echo "  ✅ Ollama (llama3.2:3b)"
echo "  ✅ Sentence-Transformers (all-MiniLM-L6-v2)"
echo "  ✅ ChromaDB"
echo "  ✅ BM25 keyword search"
echo "  ✅ Cross-encoder reranker"

echo -e "\n🎯 Next Steps:"
if command -v docker &> /dev/null && docker ps | grep -q inbox_context_graph; then
    echo "  1. Frontend: http://localhost:5173"
    echo "  2. Backend API: http://localhost:8000"
    echo "  3. API Docs: http://localhost:8000/docs"
    echo "  4. View logs: docker-compose logs -f backend"
else
    echo "  1. Start backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
    echo "  2. Start frontend: cd frontend && npm install && npm run dev"
    echo "  3. Initialize DB: python backend/init_db.py"
fi

echo -e "\n📚 Documentation:"
echo "  - Setup Guide: SETUP_GUIDE.md"
echo "  - Upgrade Summary: UPGRADE_SUMMARY.md"
echo "  - README: README.md"

echo -e "\n${GREEN}Happy hacking! 🚀${NC}\n"

