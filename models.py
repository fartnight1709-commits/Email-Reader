from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Category(str, Enum):
    FINANCIAL = "FINANCIAL"
    CLIENTS = "CLIENTS"
    REGULAR = "REGULAR"
    NEWS = "NEWS"

class PriorityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"

class EmailAnalysis(BaseModel):
    summary_executive: str = Field(description="1-line summary")
    summary_bullets: List[str] = Field(description="Core facts")
    category: Category # The new folder logic
    priority: PriorityLevel
    priority_reasoning: str
    action_items: List[str]
    suggested_reply: str
    confidence_score: int
