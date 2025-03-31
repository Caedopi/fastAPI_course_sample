from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from ...schemas.todo_request import TodoRequest
from ...crud import todos_crud as tc
from ...db.session import get_db
from ...core.security import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    output = await tc.get_todos(db, user.get("id"))
    return output


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    output = await tc.get_todo_by_id(db, todo_id, user.get("id"))
    if output is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return output


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=404, detail="No user")
    result = await tc.create_todo(db, todo_request, user.get("id"))
    if result:
        return
    raise HTTPException(status_code=404, detail="Unhandled exception")


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    result = await tc.update_todo(db, todo_id, todo_request, user_id=user.get("id"))
    if result:
        return
    raise HTTPException(status_code=404, detail="Entry not found")


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    result = await tc.delete_todo(db, todo_id, user.get("id"))
    if result:
        return
    raise HTTPException(status_code=404, detail="Entry not found")
