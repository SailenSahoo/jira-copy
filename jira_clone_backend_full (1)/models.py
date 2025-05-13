
from pydantic import BaseModel
from typing import List, Optional

class Comment(BaseModel):
    author: str
    body: str
    created: str

class CustomFields(BaseModel):
    status: Optional[str]
    priority: Optional[str]
    assignee: Optional[str]
    reporter: Optional[str]

class Issue(BaseModel):
    key: str
    summary: str
    description: Optional[str]
    customFields: CustomFields
    comments: List[Comment] = []

class Project(BaseModel):
    name: str
    issues: List[Issue]
