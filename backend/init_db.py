"""Initialize database with mock messages"""
from database import SessionLocal, engine
from models import Base, Message
from mock_data import MOCK_MESSAGES
from embeddings import get_embedding
from vector_store import get_vector_store
from chunker import get_chunker
from keyword_search import get_keyword_searcher
import uuid

# Create all tables
Base.metadata.create_all(bind=engine)

def init_messages():
    """Load mock messages into database and vector store"""
    db = SessionLocal()
    
    # Check if messages already exist
    existing = db.query(Message).count()
    if existing > 0:
        print(f"Database already has {existing} messages. Skipping initialization.")
        db.close()
        return
    
    print("Initializing database with mock messages...")
    
    # Get services
    vector_store = get_vector_store()
    chunker = get_chunker()
    
    messages = []
    all_chunks = []
    
    for msg_data in MOCK_MESSAGES:
        # Generate embedding for semantic search
        embedding = get_embedding(msg_data["content"])
        
        message = Message(
            id=str(uuid.uuid4()),
            sender_name=msg_data["sender_name"],
            sender_type=msg_data["sender_type"],
            channel=msg_data["channel"],
            subject=msg_data.get("subject"),
            content=msg_data["content"],
            embedding=embedding,
        )
        db.add(message)
        messages.append(message)
        
        # Chunk message for vector store
        msg_dict = {
            "id": message.id,
            "sender_name": message.sender_name,
            "sender_type": message.sender_type,
            "channel": message.channel,
            "subject": message.subject,
            "content": message.content,
            "timestamp": message.timestamp
        }
        chunks = chunker.chunk_message(msg_dict)
        all_chunks.extend(chunks)
    
    db.commit()
    print(f"✅ Added {len(MOCK_MESSAGES)} messages to PostgreSQL")
    
    # Add to vector store
    print("Adding chunks to vector store...")
    for chunk in all_chunks:
        chunk_embedding = get_embedding(chunk["text"])
        vector_store.store(
            id=chunk["chunk_id"],
            text=chunk["text"],
            embedding=chunk_embedding,
            metadata=chunk["metadata"]
        )
    
    print(f"✅ Added {len(all_chunks)} chunks to ChromaDB")
    
    # Index for keyword search
    print("Building keyword search index...")
    keyword_searcher = get_keyword_searcher()
    msg_dicts = [{
        "id": m.id,
        "content": m.content,
        "subject": m.subject,
        "sender_name": m.sender_name,
        "sender_type": m.sender_type,
        "channel": m.channel,
        "timestamp": m.timestamp
    } for m in messages]
    keyword_searcher.index_messages(msg_dicts)
    print(f"✅ Indexed {len(messages)} messages for keyword search")
    
    db.close()
    print(f"\n🎉 Initialization complete! Ready to use.")


if __name__ == "__main__":
    init_messages()

