from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import JiraAction

router = APIRouter(prefix="/comments", tags=["Comments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/issue/{issue_id}")
def get_comments_for_issue(issue_id: int, db: Session = Depends(get_db)):
    return db.query(JiraAction).filter(JiraAction.issueid == issue_id).all()