from fastapi import APIRouter
from connection import get_db_connection

router = APIRouter()

@router.get("/comments")
def get_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ja.issueid, ja.author, ja.actionbody, ja.created
        FROM jiraaction ja
        JOIN jiraissue ji ON ja.issueid = ji.id
        WHERE ja.actiontype = 'comment'
        AND ji.archived = '1'
    """)
    comments = []
    for row in cursor.fetchall():
        comments.append({
            "issueId": row[0],
            "author": row[1],
            "body": row[2],
            "created": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None
        })
    cursor.close()
    conn.close()
    return comments
