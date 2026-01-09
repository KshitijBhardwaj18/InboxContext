"""Initialize database with mock messages"""
from database import SessionLocal, engine
from models import Base, Message
from mock_data import MOCK_MESSAGES
from embeddings import get_embedding
import uuid

# Create all tables
Base.metadata.create_all(bind=engine)

def init_messages():
    """Load mock messages into database"""
    db = SessionLocal()
    
    # Check if messages already exist
    existing = db.query(Message).count()
    if existing > 0:
        print(f"Database already has {existing} messages. Skipping initialization.")
        db.close()
        return
    
    print("Initializing database with mock messages...")
    
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
    
    db.commit()
    print(f"Added {len(MOCK_MESSAGES)} messages to database.")
    db.close()


if __name__ == "__main__":
    init_messages()

