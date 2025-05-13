from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import JiraIssue

router = APIRouter(prefix="/issues", tags=["Issues"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def fetch_archived_issues(db: Session = Depends(get_db)):
    return db.query(JiraIssue).filter(JiraIssue.archived == "Y").all()