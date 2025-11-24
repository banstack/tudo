from sqlmodel import Session, select
from app.models import Todo, Priority
from app.schemas import TodoCreate, TodoUpdate
from typing import List, Optional
from datetime import datetime

def create_todo(session: Session, todo: TodoCreate) -> Todo:
    db_todo = Todo(**todo.model_dump())
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# Get multiple todos with hard limit of 100
def get_todos(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[Priority] = None
) -> List[Todo]:
    query = select(Todo)

    # Check if completed is true
    if completed is not None:
        query = query.where(Todo.completed == completed)

    # Check if priority is equal to priority
    if priority is not None:
        query = query.where(Todo.priority == priority)
    
    query = query.offset(skip).limit(limit).order_by(Todo.created_at.desc())

    todos = session.exec(query).all()
    return todos

def get_todo(session: Session, todo_id: int) -> Optional[Todo]:
    return session.get(Todo, todo_id)

def update_todo(session: Session, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
    db_todo = session.get(Todo, todo_id)

    if not db_todo:
        return None

    update_data = todo_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db_todo.updated_at = datetime.utcnow()

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(session: Session, todo_id: int) -> bool:
    # Provide passed in Todo model, with unique todo_id 
    db_todo = session.get(Todo, todo_id)

    if not db_todo:
        return False
    
    session.delete(db_todo)
    session.commit()
    return True

def toggle_todo_completion(session: Session, todo_id: int) -> Optional[Todo]:
    db_todo = session.get(Todo, todo_id)

    if not db_todo:
        return None
    
    db_todo.completed = not db_todo.completed
    db_todo.updated_at = datetime.utcnow()

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
