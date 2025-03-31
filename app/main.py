from fastapi import FastAPI
from .api.routers import todos, auth, admin, users
from .db.session import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="Todos", version="1.0.0")

    Base.metadata.create_all(bind=engine)
    app.include_router(auth.router)
    app.include_router(todos.router)
    app.include_router(users.router)
    app.include_router(admin.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
