from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Environment variable which looks for file .env in production in get it done using export
    """
    
    pg_database_host:str
    pg_database_port:str
    pg_database_password:str
    pg_database_name:str
    pg_database_username:str
    jwt_secret_key:str
    jwt_algorithm:str
    jwt_token_expired_minutes:int

    class Config:
        env_file=".env"

settings = Settings()