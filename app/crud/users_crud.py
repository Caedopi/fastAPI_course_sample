from sqlalchemy.orm import Session
from typing_extensions import Any

from ..models.user import Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Lolek2 1234
async def create_user(db: Session, user_request) -> bool:
    user_data = user_request.dict(exclude_unset=True)
    user_data["hashed_password"] = bcrypt_context.hash(user_data.pop("password"))
    user_data.setdefault("is_active", True)
    user_model = Users(**user_data)

    db.add(user_model)
    db.commit()
    return True


async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


async def get_user_data(db: Session, username: str) -> Any:
    user = await get_user(db, username)
    if not user:
        return False
    return user


async def update_password(db: Session, username: str, old_password: str, new_password: str) -> str:
    user = await get_user(db, username)
    if not user:
        return "User not found"
    do_old_passwords_match: bool = bcrypt_context.verify(old_password, user.hashed_password)
    if not do_old_passwords_match:
        return "Old passwords do not match, please check again"
    user.hashed_password = bcrypt_context.hash(new_password)
    db.add(user)
    db.commit()
    return "ok"


async def get_user(db, username):
    return db.query(Users).filter(Users.username == username).first()
