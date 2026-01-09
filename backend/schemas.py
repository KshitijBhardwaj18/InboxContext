from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MessageBase(BaseModel):
    sender_name: str
    sender_type: str
    channel: str
    subject: Optional[str] = None
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AgentSuggestion(BaseModel):
    action: str  # reply_now, reply_later, ignore
    tone: str  # neutral, warm, formal


class HumanAction(BaseModel):
    action: str
    tone: str


class ContextUsed(BaseModel):
    sender_type: str
    similar_decisions: List[str]


class DecisionTraceCreate(BaseModel):
    message_id: str
    agent_suggestion: AgentSuggestion
    human_action: HumanAction
    context_used: ContextUsed
    why: str


class DecisionTrace(BaseModel):
    decision_id: str
    message_id: str
    agent_suggestion: AgentSuggestion
    human_action: HumanAction
    context_used: ContextUsed
    why: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AgentResponse(BaseModel):
    action: str
    tone: str
    reasoning: str
    precedent_count: int
    similar_decisions: List[str]


class GraphNodeResponse(BaseModel):
    id: str
    type: str
    label: str
    
    class Config:
        from_attributes = True


class GraphEdgeResponse(BaseModel):
    id: str
    source: str
    target: str
    type: str
    
    class Config:
        from_attributes = True


class GraphResponse(BaseModel):
    nodes: List[GraphNodeResponse]
    edges: List[GraphEdgeResponse]

