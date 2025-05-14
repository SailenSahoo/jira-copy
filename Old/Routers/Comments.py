from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.connection import get_db_connection
from db.queries import fetch_comments_query

router = APIRouter()

@router.get("/fetch-comments")
def fetch_comments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(fetch_comments_query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        comments = []
        for row in rows:
            issue_id, author, body, created = row
            comments.append({
                "issueId": issue_id,
                "author": author,
                "body": body,
                "created": str(created)
            })

        return JSONResponse(content=comments)

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
