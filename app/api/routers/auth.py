from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from ...schemas.user_request import UserRequest
from ...crud import users_crud as uc
from ...db.session import get_db
from ...core import security as sec

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
db_dependency = Annotated[Session, Depends(get_db)]
form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserRequest):
    result = await uc.create_user(db, create_user_request)
    if result:
        return
    raise HTTPException(status_code=404, detail="Unhandled exception")


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login_for_access_token(db: db_dependency, form_data: form_dependency):
    result = await uc.authenticate_user(db, form_data.username, form_data.password)
    if not result:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No validation")
    token = sec.create_access_token(result.username, result.id, result.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
