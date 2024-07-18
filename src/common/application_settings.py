import os
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    SettingsConfigDict
)
# from common.app_configuration_settings_source import AppConfigurationSettingsSource
from typing import Optional

class ApplicationSettings(BaseSettings):
    
    GLOBAL__ENVIRONMENT: str
    OPENAI_API_KEY: str
    CLAUDE_API_KEY: Optional[str] = None
    OPENAI_ORG_ID: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    OPENAI_API_VERSION: str
 
    SQL_SERVER__HOST: str 
    SQL_SERVER__PORT: int 
    SQL_SERVER__USERNAME: str 
    SQL_SERVER__PASSWORD: str 
    SQL_SERVER__NAME: str 
    
    class Config:
        env_file = os.getenv('GLOBAL__ENVIRONMENT')
        env_file_encoding = "utf-8"
        extra="ignore"