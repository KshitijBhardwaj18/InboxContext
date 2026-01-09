# API Reference

Quick reference for all endpoints and their usage.

## Base URLs

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## Endpoints

### Health Check

#### GET `/`

Check if the API is running.

**Response:**

```json
{
  "message": "Inbox Context Graph API"
}
```

**Example:**

```bash
curl http://localhost:8000/
```

---

### Messages

#### GET `/messages`

Get all inbox messages.

**Response:**

```json
[
  {
    "id": "uuid",
    "sender_name": "Sarah Chen",
    "sender_type": "investor",
    "channel": "email",
    "subject": "Quick check-in on metrics",
    "content": "Hey! Hope you're doing well...",
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

**Example:**

```bash
curl http://localhost:8000/messages
```

---

#### GET `/messages/{message_id}`

Get a specific message.

**Parameters:**

- `message_id` (path): Message UUID

**Response:**

```json
{
  "id": "uuid",
  "sender_name": "Sarah Chen",
  "sender_type": "investor",
  "channel": "email",
  "subject": "Quick check-in on metrics",
  "content": "Hey! Hope you're doing well...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Example:**

```bash
curl http://localhost:8000/messages/abc-123-def
```

---

### Agent Suggestions

#### POST `/agent/suggest/{message_id}`

Get AI agent suggestion for a message.

**Parameters:**

- `message_id` (path): Message UUID

**Response:**

```json
{
  "action": "reply_now",
  "tone": "warm",
  "reasoning": "Based on 4 prior investor message(s), you usually chose 'warm' tone. Applying that precedent.",
  "precedent_count": 4,
  "similar_decisions": ["dec_123", "dec_456", "dec_789", "dec_012"]
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/agent/suggest/abc-123-def
```

**Python:**

```python
import requests

response = requests.post("http://localhost:8000/agent/suggest/abc-123-def")
suggestion = response.json()

print(f"Agent suggests: {suggestion['action']} with {suggestion['tone']} tone")
print(f"Based on {suggestion['precedent_count']} precedents")
```

---

### Decisions

#### POST `/decisions`

Capture a human decision trace.

**Request Body:**

```json
{
  "message_id": "abc-123-def",
  "agent_suggestion": {
    "action": "reply_now",
    "tone": "neutral"
  },
  "human_action": {
    "action": "reply_now",
    "tone": "warm"
  },
  "context_used": {
    "sender_type": "investor",
    "similar_decisions": ["dec_123", "dec_456"]
  },
  "why": "Based on 2 prior investor messages, you usually replied warmly"
}
```

**Response:**

```json
{
  "decision_id": "uuid",
  "message_id": "abc-123-def",
  "agent_suggestion": {
    "action": "reply_now",
    "tone": "neutral"
  },
  "human_action": {
    "action": "reply_now",
    "tone": "warm"
  },
  "context_used": {
    "sender_type": "investor",
    "similar_decisions": ["dec_123", "dec_456"]
  },
  "why": "Based on 2 prior investor messages...",
  "timestamp": "2024-01-15T10:35:00Z"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/decisions \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "abc-123-def",
    "agent_suggestion": {"action": "reply_now", "tone": "neutral"},
    "human_action": {"action": "reply_now", "tone": "warm"},
    "context_used": {
      "sender_type": "investor",
      "similar_decisions": []
    },
    "why": "First decision"
  }'
```

---

#### GET `/decisions`

Get all decision traces.

**Response:**

```json
[
  {
    "decision_id": "uuid",
    "message_id": "msg_123",
    "agent_suggestion": { "action": "reply_now", "tone": "neutral" },
    "human_action": { "action": "reply_now", "tone": "warm" },
    "context_used": {
      "sender_type": "investor",
      "similar_decisions": []
    },
    "why": "No precedent found. Using default logic for investor.",
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

**Example:**

```bash
curl http://localhost:8000/decisions
```

---

### Context Graph

#### GET `/graph`

Get the context graph (nodes and edges).

**Response:**

```json
{
  "nodes": [
    {
      "id": "msg_abc12345",
      "type": "message",
      "label": "Sarah Chen\ninvestor"
    },
    {
      "id": "dec_def67890",
      "type": "decision",
      "label": "Decision\nreply_now"
    },
    {
      "id": "action_reply_now",
      "type": "action",
      "label": "reply_now"
    },
    {
      "id": "tone_warm",
      "type": "tone",
      "label": "warm"
    },
    {
      "id": "sender_investor",
      "type": "sender_type",
      "label": "investor"
    }
  ],
  "edges": [
    {
      "id": "edge_123",
      "source": "msg_abc12345",
      "target": "dec_def67890",
      "type": "has_decision"
    },
    {
      "id": "edge_456",
      "source": "dec_def67890",
      "target": "action_reply_now",
      "type": "chose_action"
    },
    {
      "id": "edge_789",
      "source": "dec_def67890",
      "target": "tone_warm",
      "type": "chose_tone"
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/graph
```

---

### Demo Control

#### POST `/reset`

Reset all decisions and graph data (keeps messages).

**Response:**

```json
{
  "message": "Demo reset complete"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/reset
```

---

## Data Schemas

### Message

```typescript
{
  id: string;              // UUID
  sender_name: string;     // e.g., "Sarah Chen"
  sender_type: string;     // "investor" | "sales" | "support"
  channel: string;         // "email" | "slack" | "discord"
  subject?: string;        // Optional subject line
  content: string;         // Message body
  timestamp: string;       // ISO8601 datetime
}
```

### AgentSuggestion

```typescript
{
  action: string; // "reply_now" | "reply_later" | "ignore"
  tone: string; // "neutral" | "warm" | "formal"
}
```

### HumanAction

```typescript
{
  action: string; // "reply_now" | "reply_later" | "ignore"
  tone: string; // "neutral" | "warm" | "formal"
}
```

### ContextUsed

```typescript
{
  sender_type: string;     // "investor" | "sales" | "support"
  similar_decisions: string[];  // Array of decision IDs
}
```

### DecisionTrace

```typescript
{
  decision_id: string; // UUID
  message_id: string; // Message UUID
  agent_suggestion: AgentSuggestion;
  human_action: HumanAction;
  context_used: ContextUsed;
  why: string; // Reasoning string
  timestamp: string; // ISO8601 datetime
}
```

### GraphNode

```typescript
{
  id: string; // Node ID
  type: string; // "message" | "decision" | "action" | "tone" | "sender_type"
  label: string; // Display label
}
```

### GraphEdge

```typescript
{
  id: string; // Edge ID
  source: string; // Source node ID
  target: string; // Target node ID
  type: string; // "has_decision" | "chose_action" | "chose_tone" | etc.
}
```

---

## Example Workflows

### Workflow 1: Get Suggestion and Capture Decision

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Get messages
messages = requests.get(f"{BASE_URL}/messages").json()
message = messages[0]

# 2. Get agent suggestion
suggestion = requests.post(
    f"{BASE_URL}/agent/suggest/{message['id']}"
).json()

print(f"Agent suggests: {suggestion['action']} with {suggestion['tone']} tone")
print(f"Reasoning: {suggestion['reasoning']}")

# 3. Capture human decision (with override)
decision_data = {
    "message_id": message["id"],
    "agent_suggestion": {
        "action": suggestion["action"],
        "tone": suggestion["tone"]
    },
    "human_action": {
        "action": "reply_now",
        "tone": "warm"  # Override!
    },
    "context_used": {
        "sender_type": message["sender_type"],
        "similar_decisions": suggestion["similar_decisions"]
    },
    "why": suggestion["reasoning"]
}

decision = requests.post(
    f"{BASE_URL}/decisions",
    json=decision_data
).json()

print(f"Decision captured: {decision['decision_id']}")
```

### Workflow 2: Build Precedent and Test Learning

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Reset demo
requests.post(f"{BASE_URL}/reset")
print("Demo reset")

# 2. Get all investor messages
messages = requests.get(f"{BASE_URL}/messages").json()
investor_msgs = [m for m in messages if m["sender_type"] == "investor"]

# 3. Make 4 decisions with consistent overrides
for i, msg in enumerate(investor_msgs[:4], 1):
    # Get suggestion
    sugg = requests.post(f"{BASE_URL}/agent/suggest/{msg['id']}").json()

    # Capture decision (always override to warm)
    decision_data = {
        "message_id": msg["id"],
        "agent_suggestion": {"action": sugg["action"], "tone": sugg["tone"]},
        "human_action": {"action": "reply_now", "tone": "warm"},
        "context_used": {
            "sender_type": msg["sender_type"],
            "similar_decisions": sugg["similar_decisions"]
        },
        "why": sugg["reasoning"]
    }
    requests.post(f"{BASE_URL}/decisions", json=decision_data)

    print(f"Decision {i}/4: precedent_count = {sugg['precedent_count']}")
    time.sleep(0.5)

# 4. Test 5th message - agent should have learned!
if len(investor_msgs) > 4:
    test_msg = investor_msgs[4]
    sugg = requests.post(f"{BASE_URL}/agent/suggest/{test_msg['id']}").json()

    print(f"\n🎉 Agent learned! precedent_count = {sugg['precedent_count']}")
    print(f"Suggested: {sugg['action']} with {sugg['tone']} tone")
    print(f"Reasoning: {sugg['reasoning']}")
```

### Workflow 3: Visualize the Graph

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Get graph data
graph = requests.get(f"{BASE_URL}/graph").json()

print(f"Graph has {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")

# Print node types
node_types = {}
for node in graph['nodes']:
    node_type = node['type']
    node_types[node_type] = node_types.get(node_type, 0) + 1

print("\nNode distribution:")
for node_type, count in node_types.items():
    print(f"  {node_type}: {count}")

# Print precedent edges
precedent_edges = [e for e in graph['edges'] if e['type'] == 'based_on_precedent']
print(f"\nPrecedent connections: {len(precedent_edges)}")
```

---

## Interactive API Docs

Visit http://localhost:8000/docs for interactive Swagger UI where you can:

- Browse all endpoints
- Try API calls directly in the browser
- See request/response schemas
- Download OpenAPI spec

---

## Rate Limiting

**None!** This is a demo system. Feel free to hammer the API.

## Authentication

**None!** This is a demo system. All endpoints are public.

## CORS

Configured to allow:

- `http://localhost:5173` (frontend dev server)
- `http://localhost:3000` (alternative frontend port)

## Error Responses

All errors return JSON:

```json
{
  "detail": "Error message here"
}
```

Common status codes:

- `404` - Resource not found
- `422` - Validation error (bad request body)
- `500` - Server error

---

**Need more details?** Check [ARCHITECTURE.md](ARCHITECTURE.md) for implementation details.
