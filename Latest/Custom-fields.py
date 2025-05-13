from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import CustomField

router = APIRouter()

@router.get("/custom-fields")
def get_custom_fields(db: Session = Depends(get_db)):
    return db.query(CustomField).all()
