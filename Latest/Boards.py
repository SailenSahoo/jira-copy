from fastapi import APIRouter
from connection import get_db_connection

router = APIRouter()

@router.get("/boards")
def get_boards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description FROM board
    """)
    boards = []
    for row in cursor.fetchall():
        boards.append({
            "id": row[0],
            "name": row[1],
            "description": row[2]
        })
    cursor.close()
    conn.close()
    return boards
