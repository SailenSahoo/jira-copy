# models.py

from pydantic import BaseModel
from typing import List, Optional


class Comment(BaseModel):
    issue_id: int
    author: Optional[str]
    body: Optional[str]
    created: Optional[str]

    class Config:
        orm_mode = True


class CustomField(BaseModel):
    issue_id: int
    field_name: str
    field_value: Optional[str]

    class Config:
        orm_mode = True


class Issue(BaseModel):
    key: str
    summary: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    issue_type: Optional[str]
    assignee: Optional[str]
    reporter: Optional[str]
    created: Optional[str]
    updated: Optional[str]
    custom_fields: List[CustomField] = []
    comments: List[Comment] = []

    class Config:
        orm_mode = True


class Project(BaseModel):
    id: int
    name: str
    key: str
    issues: List[Issue] = []

    class Config:
        orm_mode = True


class Board(BaseModel):
    board_id: int
    name: Optional[str]
    owner_user_name: Optional[str]
    saved_filter_id: Optional[int]
    card_color_strategy: Optional[str]
    kan_plan_enabled: Optional[str]
    show_days_in_column: Optional[str]
    sprints_enabled: Optional[str]
    sprint_markers_migrated: Optional[str]
    swimlane_strategy: Optional[str]
    show_epic_as_panel: Optional[str]
    old_done_issue_cutoff: Optional[int]
    refined_velocity_active: Optional[str]

    class Config:
        orm_mode = True
