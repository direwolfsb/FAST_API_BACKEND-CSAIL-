from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List

class ModelName(str, Enum):
    GPT4_O = "gpt-4o"
    GPT4_O_MINI = "gpt-4o-mini"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4_O_MINI)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName
    sources: List[str]

class MessageEntry(BaseModel):
    user_query: str
    gpt_response: str
    sources: List[str]

class SessionHistoryResponse(BaseModel):
    session_id: str
    history: List[MessageEntry]