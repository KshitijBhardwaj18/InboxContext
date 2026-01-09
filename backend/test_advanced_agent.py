"""Test the upgraded intelligent agent"""
import sys
from database import SessionLocal
from models import Message
from agent import AgentEngine
import json


def test_agent_intelligence():
    """Test the new intelligent agent with various message types"""
    
    db = SessionLocal()
    
    try:
        # Get some test messages
        messages = db.query(Message).limit(5).all()
        
        if not messages:
            print("❌ No messages found in database. Run init_db.py first.")
            return
        
        # Initialize agent with LLM
        print("🚀 Initializing AgentEngine with LLM...")
        agent = AgentEngine(db, use_llm=True)
        
        print("\n" + "="*80)
        print("TESTING INTELLIGENT AGENT SUGGESTIONS")
        print("="*80)
        
        for i, message in enumerate(messages, 1):
            print(f"\n📧 TEST {i}: Message from {message.sender_name} ({message.sender_type})")
            print(f"Subject: {message.subject or 'N/A'}")
            print(f"Content: {message.content[:100]}...")
            print("-" * 80)
            
            # Get suggestion
            suggestion = agent.get_suggestion(message)
            
            # Display results
            print(f"\n✅ AGENT SUGGESTION:")
            print(f"  Action: {suggestion['action'].upper()}")
            print(f"  Tone: {suggestion['tone'].upper()}")
            print(f"  Precedent Count: {suggestion['precedent_count']}")
            
            print(f"\n💭 REASONING:")
            print(f"  {suggestion['reasoning']}")
            
            # Show message analysis
            if suggestion.get('message_analysis'):
                analysis = suggestion['message_analysis']
                print(f"\n🔍 MESSAGE ANALYSIS:")
                print(f"  Intent: {analysis.get('intent', 'N/A')}")
                print(f"  Topics: {', '.join(analysis.get('topics', ['N/A']))}")
                print(f"  Urgency: {analysis.get('urgency', 'N/A')}")
                print(f"  Requires Action: {analysis.get('requires_action', 'N/A')}")
            
            # Show draft if available
            if suggestion.get('draft_response'):
                print(f"\n✍️  DRAFT RESPONSE:")
                print(f"  {suggestion['draft_response']}")
            
            # Show context sources
            if suggestion.get('context_sources'):
                print(f"\n📚 CONTEXT SOURCES:")
                for source in suggestion['context_sources']:
                    print(f"  - {source}")
            
            print("\n" + "="*80)
            
            # Only test first 3 to avoid too much LLM usage
            if i >= 3:
                break
        
        print("\n✅ Agent testing complete!")
        print("\nThe agent now:")
        print("  ✓ Analyzes message intent and urgency")
        print("  ✓ Retrieves relevant context using hybrid search")
        print("  ✓ Makes LLM-powered decisions with reasoning")
        print("  ✓ Generates contextual draft responses")
        print("  ✓ References specific precedents in reasoning")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()


def test_without_llm():
    """Test agent fallback without LLM"""
    
    db = SessionLocal()
    
    try:
        print("\n🔄 Testing agent WITHOUT LLM (fallback mode)...")
        agent = AgentEngine(db, use_llm=False)
        
        message = db.query(Message).first()
        if message:
            suggestion = agent.get_suggestion(message)
            print(f"\nFallback suggestion: {suggestion['action']} with {suggestion['tone']} tone")
            print(f"Reasoning: {suggestion['reasoning']}")
        
    finally:
        db.close()


if __name__ == "__main__":
    print("🧪 Testing Advanced Agent System\n")
    
    # Check if --no-llm flag is passed
    if "--no-llm" in sys.argv:
        test_without_llm()
    else:
        test_agent_intelligence()
        
        # Also test fallback
        print("\n" + "="*80)
        test_without_llm()

