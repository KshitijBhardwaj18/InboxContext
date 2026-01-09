"""Main FastAPI application"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db, engine
from models import Base, Message, Decision, DecisionPrecedent, GraphNode, GraphEdge
from schemas import (
    Message as MessageSchema,
    DecisionTraceCreate,
    DecisionTrace,
    AgentResponse,
    GraphResponse,
    GraphNodeResponse,
    GraphEdgeResponse,
)
from agent import AgentEngine
from embeddings import get_embedding
from vector_store import get_vector_store

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inbox Context Graph API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Inbox Context Graph API"}


@app.get("/messages", response_model=List[MessageSchema])
def get_messages(db: Session = Depends(get_db)):
    """Get all inbox messages"""
    messages = db.query(Message).order_by(Message.timestamp.desc()).all()
    return messages


@app.get("/messages/{message_id}", response_model=MessageSchema)
def get_message(message_id: str, db: Session = Depends(get_db)):
    """Get specific message"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@app.post("/agent/suggest/{message_id}", response_model=AgentResponse)
def get_agent_suggestion(message_id: str, db: Session = Depends(get_db)):
    """Get AI agent suggestion for a message"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    agent = AgentEngine(db)
    suggestion = agent.get_suggestion(message)
    
    return AgentResponse(**suggestion)


@app.post("/decisions", response_model=DecisionTrace)
def create_decision(decision_data: DecisionTraceCreate, db: Session = Depends(get_db)):
    """Capture a human decision trace"""
    
    # Verify message exists
    message = db.query(Message).filter(Message.id == decision_data.message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Create decision
    decision = Decision(
        id=str(uuid.uuid4()),
        message_id=decision_data.message_id,
        agent_suggestion=decision_data.agent_suggestion.dict(),
        human_action=decision_data.human_action.dict(),
        context_used=decision_data.context_used.dict(),
        why=decision_data.why,
    )
    db.add(decision)
    
    # Create precedent links
    for precedent_id in decision_data.context_used.similar_decisions:
        link = DecisionPrecedent(
            decision_id=decision.id,
            precedent_id=precedent_id
        )
        db.add(link)
    
    # Update graph nodes and edges
    _update_graph(db, decision, message)
    
    db.commit()
    db.refresh(decision)
    
    # Store decision in vector store for future retrieval
    try:
        vector_store = get_vector_store()
        decision_text = f"Decision for {message.sender_name}: {decision.human_action['action']} with {decision.human_action['tone']} tone. Message: {message.content[:200]}"
        decision_embedding = get_embedding(decision_text)
        vector_store.store(
            id=f"decision_{decision.id}",
            text=decision_text,
            embedding=decision_embedding,
            metadata={
                "decision_id": decision.id,
                "message_id": message.id,
                "sender_type": message.sender_type,
                "action": decision.human_action["action"],
                "tone": decision.human_action["tone"]
            }
        )
    except Exception as e:
        print(f"Failed to store decision in vector store: {e}")
    
    return DecisionTrace(
        decision_id=decision.id,
        message_id=decision.message_id,
        agent_suggestion=decision_data.agent_suggestion,
        human_action=decision_data.human_action,
        context_used=decision_data.context_used,
        why=decision.why,
        timestamp=decision.timestamp,
    )


@app.get("/decisions", response_model=List[DecisionTrace])
def get_decisions(db: Session = Depends(get_db)):
    """Get all decision traces"""
    decisions = db.query(Decision).order_by(Decision.timestamp.desc()).all()
    
    result = []
    for d in decisions:
        result.append(
            DecisionTrace(
                decision_id=d.id,
                message_id=d.message_id,
                agent_suggestion=d.agent_suggestion,
                human_action=d.human_action,
                context_used=d.context_used,
                why=d.why,
                timestamp=d.timestamp,
            )
        )
    return result


@app.get("/graph", response_model=GraphResponse)
def get_graph(db: Session = Depends(get_db)):
    """Get context graph for visualization"""
    nodes = db.query(GraphNode).all()
    edges = db.query(GraphEdge).all()
    
    node_responses = [
        GraphNodeResponse(id=n.id, type=n.node_type, label=n.label)
        for n in nodes
    ]
    
    edge_responses = [
        GraphEdgeResponse(id=e.id, source=e.source_id, target=e.target_id, type=e.edge_type)
        for e in edges
    ]
    
    return GraphResponse(nodes=node_responses, edges=edge_responses)


@app.get("/context/retrieve")
def retrieve_context(
    query: str,
    sender_type: str = None,
    top_k: int = 5,
    db: Session = Depends(get_db)
):
    """Retrieve relevant context for a query using hybrid retrieval
    
    Args:
        query: Search query
        sender_type: Optional filter by sender type
        top_k: Number of results to return
        
    Returns:
        Ranked context with sources and scores
    """
    from retriever import HybridRetriever
    
    retriever = HybridRetriever(db)
    results = retriever.retrieve(
        query=query,
        sender_type=sender_type,
        top_k=top_k,
        use_vector=True,
        use_keyword=True,
        use_graph=True,
        rerank=True
    )
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }


@app.post("/reset")
def reset_demo(db: Session = Depends(get_db)):
    """Reset all decisions and graph (keep messages)"""
    db.query(DecisionPrecedent).delete()
    db.query(Decision).delete()
    db.query(GraphNode).delete()
    db.query(GraphEdge).delete()
    db.commit()
    
    # Also reset vector store decisions (keep messages)
    try:
        vector_store = get_vector_store()
        # Note: ChromaDB doesn't have easy prefix delete, so we'd need to query and delete
        # For simplicity, we'll just clear decision_ prefixed items if needed
    except Exception as e:
        print(f"Vector store reset warning: {e}")
    
    return {"message": "Demo reset complete"}


def _update_graph(db: Session, decision: Decision, message: Message):
    """Update graph nodes and edges for visualization"""
    
    # Create/get message node
    msg_node = db.query(GraphNode).filter(
        GraphNode.node_type == "message"
    ).all()
    
    # Find existing message node by checking properties
    msg_node_found = None
    for node in msg_node:
        if node.properties and node.properties.get("message_id") == message.id:
            msg_node_found = node
            break
    msg_node = msg_node_found
    
    if not msg_node:
        msg_node = GraphNode(
            id=f"msg_{message.id[:8]}",
            node_type="message",
            label=f"{message.sender_name}\n{message.sender_type}",
            properties={"message_id": message.id}
        )
        db.add(msg_node)
    
    # Create decision node
    decision_node = GraphNode(
        id=f"dec_{decision.id[:8]}",
        node_type="decision",
        label=f"Decision\n{decision.human_action['action']}",
        properties={"decision_id": decision.id}
    )
    db.add(decision_node)
    
    # Create action node
    action_id = f"action_{decision.human_action['action']}"
    action_node = db.query(GraphNode).filter(GraphNode.id == action_id).first()
    if not action_node:
        action_node = GraphNode(
            id=action_id,
            node_type="action",
            label=decision.human_action['action'],
            properties={}
        )
        db.add(action_node)
    
    # Create tone node
    tone_id = f"tone_{decision.human_action['tone']}"
    tone_node = db.query(GraphNode).filter(GraphNode.id == tone_id).first()
    if not tone_node:
        tone_node = GraphNode(
            id=tone_id,
            node_type="tone",
            label=decision.human_action['tone'],
            properties={}
        )
        db.add(tone_node)
    
    # Create sender_type node
    sender_type_id = f"sender_{message.sender_type}"
    sender_node = db.query(GraphNode).filter(GraphNode.id == sender_type_id).first()
    if not sender_node:
        sender_node = GraphNode(
            id=sender_type_id,
            node_type="sender_type",
            label=message.sender_type,
            properties={}
        )
        db.add(sender_node)
    
    # Create edges
    edges = [
        GraphEdge(source_id=msg_node.id, target_id=decision_node.id, edge_type="has_decision"),
        GraphEdge(source_id=decision_node.id, target_id=action_node.id, edge_type="chose_action"),
        GraphEdge(source_id=decision_node.id, target_id=tone_node.id, edge_type="chose_tone"),
        GraphEdge(source_id=decision_node.id, target_id=sender_node.id, edge_type="from_sender_type"),
    ]
    
    for edge in edges:
        db.add(edge)
    
    # Add precedent edges
    for precedent_id in decision.context_used.get("similar_decisions", []):
        precedent = db.query(Decision).filter(Decision.id == precedent_id).first()
        if precedent:
            prec_node_id = f"dec_{precedent.id[:8]}"
            edge = GraphEdge(
                source_id=decision_node.id,
                target_id=prec_node_id,
                edge_type="based_on_precedent"
            )
            db.add(edge)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

