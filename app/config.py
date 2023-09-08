from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    database_port: str
    database_name: str
    database_hostname: str
    access_token_expire_mins: int
    algorithm: str
    secret_key: str = "blah"
    
    class Config:
        env_file=".env"
        
settings = Settings()

#settings.database_password, now you can access the elements like this 