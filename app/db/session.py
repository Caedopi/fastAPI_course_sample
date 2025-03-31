from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base


SQL_DATABASE_URL = "sqlite:///./todosapp.db"

engine = create_engine(SQL_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
