import os
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    SettingsConfigDict
)
# from common.app_configuration_settings_source import AppConfigurationSettingsSource
from typing import Optional

class ApplicationSettings(BaseSettings):
    #model_config = SettingsConfigDict(env_nested_delimiter="__", extra="ignore")
    
    GLOBAL__ENVIRONMENT: str
    OPENAI_API_KEY: str
    CLAUDE_API_KEY: Optional[str] = None
    #PHOENIX_PROJECT_NAME: str
    #PHOENIX_COLLECTOR_ENDPOINT: Optional[str] = None
    #PHOENIX_PORT: Optional[int] = 6006
    OPENAI_ORG_ID: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    OPENAI_API_VERSION: str
    
    # OPEN_AI_EMBEDDINGS__API_TYPE: str
    # OPEN_AI_EMBEDDINGS__API_KEY: str
    # OPEN_AI_EMBEDDINGS__AZURE_ENDPOINT: str
    # OPEN_AI_EMBEDDINGS__API_VERSION: str

    # QDRANT__ENDPOINT: str
    # QDRANT__API_KEY: str
    # QDRANT__PORT: int

    # APPLICATION_INSIGHTS__CONNECTION_STRING: str
 
    SQL_SERVER__HOST: str 
    SQL_SERVER__PORT: int 
    SQL_SERVER__USERNAME: str 
    SQL_SERVER__PASSWORD: str 
    SQL_SERVER__NAME: str 
    
    # SQL_SERVER__CONNECTION_STRING: str
    # SQL_SERVER__HOST: str = "mssql-server-preparador-dev-we-001.database.windows.net"
    # SQL_SERVER__PORT: int = 1433
    # SQL_SERVER__USERNAME: str = "user4defOP7r479X"
    # SQL_SERVER__PASSWORD: str = "v3lllscr37-244saafD-wd33434DLz"
    # SQL_SERVER__NAME: str = "preparador"
    
    class Config:
        env_file = [".env", f".env.{os.environ['GLOBAL__ENVIRONMENT']}"]
        env_file_encoding = "utf-8"
        extra="ignore"