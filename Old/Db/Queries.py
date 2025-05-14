fetch_boards_query = """
SELECT 
    id,
    name,
    owner_user_name,
    saved_filter_id,
    card_color_stratergy,
    kan_plan_enabled,
    sprints_enabled,
    swimlane_strategy,
    show_days_in_column,
    sprint_markers_migrated,
    show_epic_as_panel,
    old_done_issue_cutoff,
    refined_velocity_active
FROM
    board
"""
fetch_comments_query = """
SELECT
    issueid,
    author,
    body,
    created
FROM
    jiraaction
WHERE
    actiontype = 'comment'
"""
fetch_projects_query = """
SELECT
    id,
    pname,
    pkey,
    lead,
    description
FROM
    project
"""

