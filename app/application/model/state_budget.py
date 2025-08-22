from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Optional


class StateBudget(BaseModel):
    messages: list[HumanMessage | SystemMessage] = Field(default=[])
    requested_service_id: int = Field(default=0)
    key_words: Optional[list[str]] = Field(default=[])
    response: Optional[str] = Field(default=None)