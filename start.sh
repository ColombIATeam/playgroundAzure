#!/bin/bash

cat <<EOL > .env
OPENAI_API_KEY=sk-proj-9wwoos1Zl8owoDU9uQcRT3BlbkFJQFrpEbBptQrsmsKl9DET
OPENAI_ORG_ID=org-fb2NibLOPT5s0bPa0y2ZVkDI
AZURE_OPENAI_ENDPOINT=https://proyectoiaopenaiscdev.openai.azure.com/
OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_API_KEY=esto en realidad no se usa asi que no importa que escribas aca

GLOBAL__ENVIRONMENT=dev

WORKERS=1

SQL_SERVER__HOST=mssql-server-arc-dev-we-001.database.windows.net
SQL_SERVER__PORT=1433
SQL_SERVER__USERNAME=4d22157r479X
SQL_SERVER__PASSWORD=4-v3lllscr37-p455w0rd
SQL_SERVER__NAME=playground_prep
EOL



python src/main.py
