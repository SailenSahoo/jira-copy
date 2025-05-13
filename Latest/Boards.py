# routers/boards.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Board

router = APIRouter()

@router.get("/boards", response_model=list[Board])
def get_boards(db: Session = Depends(get_db)):
    results = db.execute("""
        SELECT
            ID AS board_id,
            NAME AS name,
            OWNER_USER_NAME AS owner_user_name,
            SAVED_FILTER_ID AS saved_filter_id,
            CARD_COLOR_STRATERGY AS card_color_strategy,
            KAN_PLAN_ENABLED AS kan_plan_enabled,
            SHOW_DAYS_IN_COLUMN AS show_days_in_column,
            SPRINTS_ENABLED AS sprints_enabled,
            SPRINT_MARKERS_MIGRATED AS sprint_markers_migrated,
            SWIMLANE_STRATEGY AS swimlane_strategy,
            SHOW_EPIC_AS_PANEL AS show_epic_as_panel,
            OLD_DONE_ISSUE_CUTOFF AS old_done_issue_cutoff,
            REFINED_VELOCITY_ACTIVE AS refined_velocity_active
        FROM AO_60DB71_RAPIDVIEW
    """)
    
    boards = [Board(**dict(row._mapping)) for row in results]
    return boards
