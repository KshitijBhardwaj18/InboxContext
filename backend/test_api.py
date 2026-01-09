"""
Quick API test script to verify the system works
Run with: python test_api.py
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Inbox Context Graph API...\n")
    
    # Test 1: Health check
    print("1️⃣ Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("   ✅ Root endpoint working")
    
    # Test 2: Get messages
    print("\n2️⃣ Testing messages endpoint...")
    response = requests.get(f"{BASE_URL}/messages")
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) > 0
    print(f"   ✅ Found {len(messages)} messages")
    
    # Test 3: Get agent suggestion
    print("\n3️⃣ Testing agent suggestion...")
    first_message = messages[0]
    response = requests.post(f"{BASE_URL}/agent/suggest/{first_message['id']}")
    assert response.status_code == 200
    suggestion = response.json()
    assert "action" in suggestion
    assert "tone" in suggestion
    assert "reasoning" in suggestion
    print(f"   ✅ Agent suggested: {suggestion['action']} with {suggestion['tone']} tone")
    print(f"   📝 Reasoning: {suggestion['reasoning']}")
    
    # Test 4: Create decision
    print("\n4️⃣ Testing decision capture...")
    decision_data = {
        "message_id": first_message["id"],
        "agent_suggestion": {
            "action": suggestion["action"],
            "tone": suggestion["tone"]
        },
        "human_action": {
            "action": "reply_now",
            "tone": "warm"
        },
        "context_used": {
            "sender_type": first_message["sender_type"],
            "similar_decisions": suggestion["similar_decisions"]
        },
        "why": suggestion["reasoning"]
    }
    response = requests.post(f"{BASE_URL}/decisions", json=decision_data)
    assert response.status_code == 200
    decision = response.json()
    assert "decision_id" in decision
    print(f"   ✅ Decision captured: {decision['decision_id']}")
    
    # Test 5: Get decisions
    print("\n5️⃣ Testing decisions list...")
    response = requests.get(f"{BASE_URL}/decisions")
    assert response.status_code == 200
    decisions = response.json()
    assert len(decisions) > 0
    print(f"   ✅ Found {len(decisions)} decision(s)")
    
    # Test 6: Get graph
    print("\n6️⃣ Testing graph endpoint...")
    response = requests.get(f"{BASE_URL}/graph")
    assert response.status_code == 200
    graph = response.json()
    assert "nodes" in graph
    assert "edges" in graph
    print(f"   ✅ Graph has {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
    
    # Test 7: Test precedent learning (make 2 more decisions)
    print("\n7️⃣ Testing precedent learning...")
    investor_messages = [m for m in messages if m["sender_type"] == "investor"][:3]
    
    for i, msg in enumerate(investor_messages[1:], start=2):
        # Get suggestion
        response = requests.post(f"{BASE_URL}/agent/suggest/{msg['id']}")
        suggestion = response.json()
        
        # Create decision (always choose warm)
        decision_data = {
            "message_id": msg["id"],
            "agent_suggestion": {
                "action": suggestion["action"],
                "tone": suggestion["tone"]
            },
            "human_action": {
                "action": "reply_now",
                "tone": "warm"
            },
            "context_used": {
                "sender_type": msg["sender_type"],
                "similar_decisions": suggestion["similar_decisions"]
            },
            "why": suggestion["reasoning"]
        }
        requests.post(f"{BASE_URL}/decisions", json=decision_data)
        print(f"   📊 Decision {i}/3: precedent_count = {suggestion['precedent_count']}")
        sleep(0.5)
    
    # Test 8: Verify learning
    print("\n8️⃣ Verifying agent learned from decisions...")
    if len(investor_messages) > 3:
        test_msg = investor_messages[3]
        response = requests.post(f"{BASE_URL}/agent/suggest/{test_msg['id']}")
        suggestion = response.json()
        
        if suggestion["precedent_count"] > 0:
            print(f"   ✅ Agent is now using precedent! (count: {suggestion['precedent_count']})")
            print(f"   🎯 Suggested: {suggestion['action']} with {suggestion['tone']} tone")
            if suggestion['tone'] == 'warm':
                print("   🎉 Agent learned to suggest 'warm' tone for investors!")
        else:
            print("   ℹ️  Not enough precedent yet (need more similar messages)")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\n💡 Next steps:")
    print("   - Open http://localhost:5173 to use the UI")
    print("   - Try making more decisions to see learning in action")
    print("   - View the Context Graph tab to visualize decisions")
    print("   - Use 'Reset Demo' to start fresh")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend at http://localhost:8000")
        print("   Make sure the backend is running:")
        print("   cd backend && source venv/bin/activate && uvicorn main:app --reload")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

