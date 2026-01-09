"""Test script for vector store and embeddings"""
from embeddings import get_embedding
from vector_store import get_vector_store
from chunker import get_chunker


def test_embeddings():
    """Test local embedding generation"""
    print("\n=== Testing Embeddings ===")
    
    text = "Hello, this is a test message about AI and machine learning."
    embedding = get_embedding(text)
    
    print(f"Text: {text}")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print(f"✅ Embedding generation working")
    
    return embedding


def test_vector_store():
    """Test vector store operations"""
    print("\n=== Testing Vector Store ===")
    
    store = get_vector_store()
    print(f"Initial count: {store.count()}")
    
    # Test store
    test_docs = [
        {
            "id": "test_1",
            "text": "Sarah Chen wants to discuss Q4 metrics and growth",
            "metadata": {"sender_type": "investor", "test": True}
        },
        {
            "id": "test_2",
            "text": "Mike is asking about enterprise pricing",
            "metadata": {"sender_type": "sales", "test": True}
        },
        {
            "id": "test_3",
            "text": "Jessica wants to sync about fundraising round",
            "metadata": {"sender_type": "investor", "test": True}
        }
    ]
    
    for doc in test_docs:
        embedding = get_embedding(doc["text"])
        store.store(
            id=doc["id"],
            text=doc["text"],
            embedding=embedding,
            metadata=doc["metadata"]
        )
    
    print(f"After storing: {store.count()} documents")
    print("✅ Document storage working")
    
    # Test search
    query = "investor metrics and growth discussion"
    query_embedding = get_embedding(query)
    
    results = store.search(
        query_embedding=query_embedding,
        n_results=2
    )
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results['ids'])} results:")
    for i, (id, doc, dist) in enumerate(zip(results['ids'], results['documents'], results['distances'])):
        print(f"  {i+1}. ID: {id}")
        print(f"     Text: {doc}")
        print(f"     Distance: {dist:.4f}")
    
    print("✅ Semantic search working")
    
    # Test filtered search
    results_filtered = store.search(
        query_embedding=query_embedding,
        n_results=5,
        where={"sender_type": "investor"}
    )
    
    print(f"\nFiltered search (investor only): {len(results_filtered['ids'])} results")
    for id in results_filtered['ids']:
        print(f"  - {id}")
    
    print("✅ Filtered search working")
    
    # Cleanup test data
    for doc in test_docs:
        store.delete(doc["id"])
    
    print(f"\nAfter cleanup: {store.count()} documents")
    print("✅ Delete working")


def test_chunker():
    """Test message chunking"""
    print("\n=== Testing Chunker ===")
    
    chunker = get_chunker()
    
    test_message = {
        "id": "msg_test",
        "sender_name": "Sarah Chen",
        "sender_type": "investor",
        "channel": "email",
        "subject": "Q4 Metrics Review",
        "content": "Hi! Hope you're doing well. I wanted to check in on this quarter's growth metrics. When you have a moment, could you share the latest dashboard? No rush, but would love to see the numbers before our board meeting next week.",
        "timestamp": "2024-01-15T10:30:00"
    }
    
    chunks = chunker.chunk_message(test_message)
    
    print(f"Message from: {test_message['sender_name']}")
    print(f"Content length: {len(test_message['content'])} chars")
    print(f"Number of chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"  ID: {chunk['chunk_id']}")
        print(f"  Text: {chunk['text'][:100]}...")
        print(f"  Metadata: {chunk['metadata']}")
    
    print("✅ Chunking working")


if __name__ == "__main__":
    print("🧪 Running Vector Store Tests...\n")
    
    try:
        test_embeddings()
        test_vector_store()
        test_chunker()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

