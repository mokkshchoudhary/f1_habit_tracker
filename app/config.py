from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url:str

    class config:
        env_file = '.env'

settings = Settings()