from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    PROJECT_NAME: str = "AutoAnalyst AI"

    class Config:
        env_file = ".env"

settings = Settings()
