from fastapi import APIRouter
from fastapi.responses import JSONResponse
from db.connection import get_db_connection
from db.queries import fetch_boards_query

router = APIRouter()

@router.get("/fetch-boards")
def fetch_boards():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(fetch_boards_query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        boards = []
        for row in rows:
            (
                id,
                name,
                owner_user_name,
                saved_filter_id,
                card_color_strategy,
                kan_plan_enabled,
                sprints_enabled,
                swimlane_strategy,
                show_days_in_column,
                sprint_markers_migrated,
                show_epic_as_panel,
                old_done_issue_cutoff,
                refined_velocity_active,
            ) = row

            boards.append({
                "id": id,
                "name": name,
                "owner": owner_user_name,
                "savedFilterId": saved_filter_id,
                "settings": {
                    "cardColorStrategy": card_color_strategy,
                    "kanPlanEnabled": kan_plan_enabled,
                    "sprintsEnabled": sprints_enabled,
                    "swimlaneStrategy": swimlane_strategy,
                    "showDaysInColumn": show_days_in_column,
                    "sprintMarkersMigrated": sprint_markers_migrated,
                    "showEpicAsPanel": show_epic_as_panel,
                    "oldDoneIssueCutoff": old_done_issue_cutoff,
                    "refinedVelocityActive": refined_velocity_active
                }
            })

        return JSONResponse(content=boards)

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
