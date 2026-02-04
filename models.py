from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PriorityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"

class EmailAnalysis(BaseModel):
    summary_executive: str = Field(description="1-line summary for high-level overview")
    summary_detailed: str = Field(description="Bullet points of core facts")
    priority: PriorityLevel
    priority_reasoning: str
    action_items: List[str]
    suggested_reply: str
    tone_detected: str
    confidence_score: float

class EmailMetadata(BaseModel):
    thread_id: str
    message_id: str
    sender_email: str
    recipient_email: str
    subject: str
    timestamp: str
