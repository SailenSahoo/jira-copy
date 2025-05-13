from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import projects, issues, comments, boards, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(issues.router)
app.include_router(comments.router)
app.include_router(boards.router)
app.include_router(users.router)

from db import SessionLocal

@app.get("/test-db")
def test_db():
    try:
        db = SessionLocal()
        db.execute("SELECT 1 FROM DUAL")
        return {"status": "Connection successful"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
