from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import issues, projects, comments, metadata
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(issues.router, prefix="/api/issues", tags=["Issues"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(metadata.router, prefix="/api/metadata", tags=["Metadata"])
