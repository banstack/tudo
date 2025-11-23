from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional

# Our bespoke Database, Models, and Schema imports
from app.database import create_db_and_tables, get_session
from app.models import Priority
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app import crud

app = FastAPI(
    title="Todo API",
    description="A simple tood application API",
    version="1.0.0"
)

# CORS middleware for frontend integration

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Tudo API",
        "dos": "/docs",
        "version": "1.0.0"
    }

@app.post("/todos/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session)
):
    """Create a new todo item"""
    return crud.create_todo(session, todo)

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    session: Session = Depends(get_session)
):
    """
        Get all todos with optional filtering
        - Completed: filter by completion status
        - priority: filter by priority level
        - skip number of items to skip (pagination
        - limit: amximum number of items to return)
    """
    return crud.get_todos(session, skip, limit, completed, priority)

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(
    todo_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID"""
    todo = crud.get_todo(session, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: Session = Depends(get_session)
):
    """Update a todo item"""
    updated_todo = crud.update_todo(session, todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found to update")
    return updated_todo

@app.post("/todos/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo(
    todo_id: int,
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a todo"""
    todo = crud.toggle_todo_completion(session, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found to toggle")
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session)
):
    """Delete a todo item"""
    success = crud.delete_todo(session, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found to delete")
    return update_todo


# TODO: to extend with time
@app.get("/stats")
def get_status(session: Session = Depends(get_session)):
    """Get statistics about todos"""
    all_todos = crud.get_todos(session, limit=1000)

    completed = sum(1 for todo in all_todos if todo.completed)
    pending = len(all_todos) - completed

    by_priority = {
        "low": sum(1 for todo in all_todos if todo.priority == Priority.LOW),
        "medium": sum(1 for todo in all_todos if todo.priority == Priority.MEDIUM),
        "high": sum(1 for todo in all_todos if todo.priority == Priority.high),
    }

    return {
        "total": len(all_todos),
        "completed": completed,
        "pending": pending,
        "by_priority": by_priority
    }