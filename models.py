from pydantic import BaseModel, Field
from enum import Enum

class Category(str, Enum):
    FINANCIAL = "FINANCIAL"
    CLIENTS = "CLIENTS"
    REGULAR = "REGULAR"
    NEWS = "NEWS"

class EmailAnalysis(BaseModel):
    summary_executive: str = Field(description="A 1-sentence bottom-line-up-front (BLUF) summary.")
    category: Category = Field(description="The vault this email belongs in based on its content.")
    suggested_reply: str = Field(description="A professional, concise email draft for the CEO to send back as well as a 1-3 sentence summary of this email.")
