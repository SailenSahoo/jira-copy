from fastapi import APIRouter
from connection import get_db_connection

router = APIRouter()

@router.get("/issues")
def get_issues():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            ji.issuenum,
            p.pkey,
            ji.summary,
            cfv_status.stringvalue AS status,
            cfv_priority.stringvalue AS priority
        FROM jiraissue ji
        JOIN project p ON ji.project = p.id
        LEFT JOIN customfieldvalue cfv_status
            ON ji.id = cfv_status.issue
            AND cfv_status.customfield = 10000  -- replace with actual status customfield id
        LEFT JOIN customfieldvalue cfv_priority
            ON ji.id = cfv_priority.issue
            AND cfv_priority.customfield = 10001  -- replace with actual priority customfield id
        WHERE ji.archived = '1'
    """)
    result = []
    for row in cursor.fetchall():
        result.append({
            "key": f"{row[1]}-{row[0]}",
            "summary": row[2],
            "customFields": {
                "status": row[3],
                "priority": row[4]
            }
        })
    cursor.close()
    conn.close()
    return result
