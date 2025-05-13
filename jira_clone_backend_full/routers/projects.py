from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Project

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()