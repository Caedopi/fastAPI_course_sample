from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "6ecab9525faa2842a50ee162b396592928525ffeb990a11382f49a30bea6c8e8"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 20

    class Config:
        env_file = ".env"


settings = Settings()
