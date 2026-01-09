#!/bin/bash

echo "🚀 Setting up Inbox Context Graph..."

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inbox_context_graph
OPENAI_API_KEY=
EOF
    echo "⚠️  Please add your OPENAI_API_KEY to backend/.env"
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure PostgreSQL is running"
echo "2. Create database: createdb inbox_context_graph"
echo "3. Add OPENAI_API_KEY to backend/.env (optional but recommended)"
echo "4. Initialize database: cd backend && python init_db.py"
echo "5. Start backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "6. Start frontend: cd frontend && npm run dev"
echo ""

