from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Priority = Literal["low", "medium", "high"]
Status = Literal["backlog", "in_progress", "blocked", "done"]


class ActionItem(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    owner: str = Field(default="Unassigned", min_length=1, max_length=100)
    due_date: date | None = None
    priority: Priority = "medium"
    evidence: str = Field(min_length=5, max_length=500)

    @field_validator("title", "owner", "evidence")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class MeetingResult(BaseModel):
    summary: str = Field(min_length=10, max_length=2000)
    decisions: list[str] = Field(default_factory=list, max_length=20)
    action_items: list[ActionItem] = Field(default_factory=list, max_length=50)
    risks: list[str] = Field(default_factory=list, max_length=20)


class Task(BaseModel):
    id: int | None = None
    meeting_id: str
    title: str = Field(min_length=3, max_length=200)
    owner: str = Field(default="Unassigned", min_length=1, max_length=100)
    due_date: date | None = None
    priority: Priority = "medium"
    status: Status = "backlog"
    evidence: str = Field(min_length=5, max_length=500)
