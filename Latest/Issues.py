from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Issue, CustomField, Comment

router = APIRouter()

@router.get("/issues")
def get_all_issues(db: Session = Depends(get_db)):
    issues_data = db.query(Issue).all()
    results = []
    for issue in issues_data:
        comments = db.query(Comment).filter(Comment.issue_id == issue.id).all()
        custom_fields = db.query(CustomField).filter(CustomField.issue_id == issue.id).all()
        results.append({
            "id": issue.id,
            "key": f"{issue.pkey}-{issue.issuenum}",
            "summary": issue.summary,
            "description": issue.description,
            "status": issue.status,
            "priority": issue.priority,
            "created": issue.created,
            "updated": issue.updated,
            "reporter": issue.reporter,
            "assignee": issue.assignee,
            "project_id": issue.project,
            "custom_fields": [
                {"field": field.customfield_name, "value": field.stringvalue}
                for field in custom_fields
            ],
            "comments": [
                {
                    "author": comment.author,
                    "body": comment.body,
                    "created": comment.created
                }
                for comment in comments
            ]
        })
    return results
