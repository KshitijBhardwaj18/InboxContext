from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    sender_name = Column(String, nullable=False)
    sender_type = Column(String, nullable=False)  # investor, sales, support
    channel = Column(String, nullable=False)  # email, slack, discord
    subject = Column(String)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    embedding = Column(JSON)  # Store as array
    
    decisions = relationship("Decision", back_populates="message")


class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    agent_suggestion = Column(JSON, nullable=False)  # {action, tone}
    human_action = Column(JSON, nullable=False)  # {action, tone}
    context_used = Column(JSON, nullable=False)  # {sender_type, similar_decisions}
    why = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("Message", back_populates="decisions")
    precedent_links = relationship(
        "DecisionPrecedent",
        foreign_keys="DecisionPrecedent.decision_id",
        back_populates="decision"
    )


class DecisionPrecedent(Base):
    """Edge table linking decisions to their precedents"""
    __tablename__ = "decision_precedents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    decision_id = Column(String, ForeignKey("decisions.id"), nullable=False)
    precedent_id = Column(String, ForeignKey("decisions.id"), nullable=False)
    
    decision = relationship("Decision", foreign_keys=[decision_id], back_populates="precedent_links")
    precedent = relationship("Decision", foreign_keys=[precedent_id])


class GraphNode(Base):
    """Flexible node table for graph visualization"""
    __tablename__ = "graph_nodes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    node_type = Column(String, nullable=False)  # message, decision, sender_type, action, tone
    label = Column(String, nullable=False)
    properties = Column(JSON)


class GraphEdge(Base):
    """Edge table for graph visualization"""
    __tablename__ = "graph_edges"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    source_id = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    edge_type = Column(String, nullable=False)  # has_decision, chose_action, chose_tone, etc.

