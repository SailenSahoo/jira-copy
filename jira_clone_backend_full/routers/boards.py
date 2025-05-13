from fastapi import APIRouter

router = APIRouter(prefix="/boards", tags=["Boards"])

@router.get("/")
def get_boards():
    return [{"id": 1, "name": "Archived Board"}]