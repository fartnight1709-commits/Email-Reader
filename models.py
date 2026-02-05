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
    summary_executive: str = Field(description="1-line executive summary of the email.")
    category: Category = Field(description="The vault this email belongs in.")
    priority: PriorityLevel = Field(description="The urgency of the communication.")
    suggested_reply: str = Field(description="A professional draft for the CEO.")
