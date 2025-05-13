from fastapi import APIRouter
from connection import get_db_connection

router = APIRouter()

@router.get("/projects")
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT p.pname
        FROM project p
        JOIN jiraissue ji ON p.id = ji.project
        WHERE ji.archived = '1'
    """)
    result = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return result
