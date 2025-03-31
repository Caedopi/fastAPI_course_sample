from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...core.security import get_current_user
from ...crud import users_crud as uc

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    result = await uc.get_user_data(db, user.get("username"))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/change_password", status_code=status.HTTP_202_ACCEPTED)
async def update_password(user: user_dependency, db: db_dependency,
                          old_password: str, new_password: str):
    result = await uc.update_password(db, user.get("username"), old_password, new_password)
    if result != "ok":
        raise HTTPException(status_code=404, detail=result)
    return True
