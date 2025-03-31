from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from ...schemas.todo_request import TodoRequest
from ...crud import todos_crud as tc
from ...db.session import get_db
from ...core.security import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user.get("role") != "admin":
        raise HTTPException(status_code=404, detail="No admin lol")
    result = await tc.get_todos(db)
    return result


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=404, detail="No admin lol")
    result = await tc.delete_todo(db, todo_id)
    if result:
        return
    raise HTTPException(status_code=404, detail="Entry not found")
