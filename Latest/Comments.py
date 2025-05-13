from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Comment

router = APIRouter()

@router.get("/comments")
def get_all_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()
