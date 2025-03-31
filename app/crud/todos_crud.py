from sqlalchemy.orm import Session
from ..models.todo import Todos
from typing import Optional


async def get_todos(db: Session, user_id: Optional[int] = None):
    query = db.query(Todos)
    if user_id is not None:
        query = query.filter(Todos.owner_id == user_id)
    return query.all()


async def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user_id
                                  ).first()


async def create_todo(db: Session, todo_request, user_id: int) -> bool:
    todo_model = Todos(**todo_request.model_dump(), owner_id=user_id)
    db.add(todo_model)
    db.commit()
    return True


async def update_todo(db: Session, todo_id: int, todo_request, user_id: int) -> bool:
    todo_model = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user_id).first()
    if not todo_model:
        return False

    update_data = todo_request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo_model, field, value)

    db.add(todo_model)
    db.commit()
    return True


async def delete_todo(db: Session, todo_id: int, user_id: Optional[int] = None) -> bool:
    query = db.query(Todos).filter(Todos.id == todo_id)
    if user_id is not None:
        query = query.filter(Todos.owner_id == user_id)
    final_item = query.first()
    if not final_item:
        return False
    db.delete(final_item)
    db.commit()
    return True
