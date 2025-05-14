from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.connection import get_db_connection
from db.queries import fetch_projects_query

router = APIRouter()

@router.get("/fetch-projects")
def fetch_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(fetch_projects_query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        projects = []
        for row in rows:
            id, pname, pkey, lead, description = row
            projects.append({
                "id": id,
                "name": pname,
                "key": pkey,
                "lead": lead,
                "description": description
            })

        return JSONResponse(content=projects)

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
