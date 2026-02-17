from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import tasks
from src.api.routes.auth import router as auth_router
from src.api.routes.chat import router as chat_router
from src.models.database import engine
from src.models import SQLModel
import uvicorn

# Create database tables
SQLModel.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="2.0.0")

# Add CORS middleware - Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Explicitly expose headers that frontend might need
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])  # Updated to remove user_id dependency since we now use auth
app.include_router(auth_router, prefix="/api", tags=["auth"])  # Include auth routes
app.include_router(chat_router, tags=["chat"])  # Include chat routes (prefix already in router)

@app.get("/")
def read_root():
    return {"message": "Task Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "task-management-api"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)