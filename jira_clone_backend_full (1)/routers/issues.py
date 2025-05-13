
from fastapi import APIRouter
from db import get_db_connection
from models import Project, Issue, CustomFields, Comment

router = APIRouter()

@router.get("/fetch-issues", response_model=list[Project])
def fetch_issues():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT p.pname as project_name, 
           ji.issuenum, 
           ji.summary, 
           ji.description, 
           st.pname as status, 
           pr.pname as priority,
           u.display_name as assignee_name,
           r.display_name as reporter_name,
           ji.id as issue_id,
           p.pkey as project_key
    FROM jiraissue ji
    JOIN project p ON ji.project = p.id
    LEFT JOIN issuestatus st ON ji.issuestatus = st.id
    LEFT JOIN priority pr ON ji.priority = pr.id
    LEFT JOIN app_user u ON ji.assignee = u.user_key
    LEFT JOIN app_user r ON ji.reporter = r.user_key
    WHERE ji.archived = '1'
    ORDER BY p.pname, ji.issuenum
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    projects = {}
    for row in rows:
        project_name = row[0]
        issue_key = f"{row[9]}-{int(row[1])}"
        issue = Issue(
            key=issue_key,
            summary=row[2],
            description=row[3],
            customFields=CustomFields(
                status=row[4],
                priority=row[5],
                assignee=row[6],
                reporter=row[7],
            ),
            comments=[]
        )
        if project_name not in projects:
            projects[project_name] = []
        projects[project_name].append(issue)

    cursor.execute("""
    SELECT ja.issueid, au.display_name, ja.body, ja.created
    FROM jiraaction ja
    LEFT JOIN app_user au ON ja.author = au.user_key
    """)
    comment_rows = cursor.fetchall()
    comment_map = {}
    for row in comment_rows:
        issue_id = row[0]
        comment = Comment(
            author=row[1],
            body=row[2],
            created=str(row[3])
        )
        if issue_id not in comment_map:
            comment_map[issue_id] = []
        comment_map[issue_id].append(comment)

    final_projects = []
    for pname, issues in projects.items():
        for issue in issues:
            issue_id = next((row[8] for row in rows if f"{row[9]}-{int(row[1])}" == issue.key), None)
            if issue_id in comment_map:
                issue.comments = comment_map[issue_id]
        final_projects.append(Project(name=pname, issues=issues))

    cursor.close()
    conn.close()

    return final_projects
