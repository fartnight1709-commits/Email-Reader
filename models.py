from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class PriorityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"

class EmailAnalysis(BaseModel):
    summary_executive: str = Field(description="1-line summary")
    summary_detailed: str = Field(description="Bullet points of core facts")
    priority: PriorityLevel
    priority_reasoning: str
    action_items: List[str]
    suggested_reply: str
    tone_detected: str
    confidence_score: float
