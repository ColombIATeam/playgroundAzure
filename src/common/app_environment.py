from enum import StrEnum


class AppEnvironment(StrEnum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"