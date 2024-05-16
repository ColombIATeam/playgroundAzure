import sys
from api.workflows.test_questions.test_workflow import TestWorkflow
from api.workflows.question_correct.question_correct_workflow import QuestionCorrectWorkflow
from api.workflows.question_incorrect.question_incorrect_workflow import QuestionIncorrectWorkflow
from common.application_settings import ApplicationSettings
from sqlalchemy import Engine, create_engine
from openai import AzureOpenAI
import logging


class DependencyContainer:
    _application_settings: ApplicationSettings
    _database_engine: Engine
    _azure_openai_client: AzureOpenAI
    _embeddings_client: AzureOpenAI

    @classmethod
    def initialize(cls) -> None:
        #logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        logging.info("Initializing DependencyContainer")
        cls._initialize_application_settings()
        cls._initialize_database_engine()
        logging.info("DependencyContainer initialized")
    
    @classmethod
    def _initialize_application_settings(cls) -> None:
        cls._application_settings = ApplicationSettings()  # type: ignore

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls._application_settings

    @classmethod
    def get_database_engine(cls) -> Engine:
        return cls._database_engine

    @classmethod
    def get_azure_openai_engine(cls) -> AzureOpenAI:
        return cls._azure_openai_client

    @classmethod
    def _initialize_database_engine(cls) -> None:
        url = f"mssql+pyodbc://{cls._application_settings.SQL_SERVER__USERNAME}:{cls._application_settings.SQL_SERVER__PASSWORD}@{cls._application_settings.SQL_SERVER__HOST}:{cls._application_settings.SQL_SERVER__PORT}/{cls._application_settings.SQL_SERVER__NAME}?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
        cls._database_engine = create_engine(url=url, echo=False)
    
    @classmethod
    def _initialize_openai_engine(cls) -> None:
        cls._azure_openai_client = AzureOpenAI(
            api_key=cls._application_settings.OPEN_AI__API_KEY,
            api_version=cls._application_settings.OPEN_AI__API_VERSION,
            azure_endpoint=cls._application_settings.OPEN_AI__AZURE_ENDPOINT,
        )

    @classmethod
    def get_question_correct_workflow(cls,eval_switch) -> QuestionCorrectWorkflow:
        logging.info("Creating QuestionCorrectWorkflow with dependencies")
        cls._initialize_openai_engine()
        return QuestionCorrectWorkflow(
            eval_switch,
            cls.get_database_engine(),
            cls.get_azure_openai_engine()
        )
    
    @classmethod
    def get_question_incorrect_workflow(cls,eval_switch) -> QuestionIncorrectWorkflow:
        logging.info("Creating QuestionIncorrectWorkflow with dependencies")
        cls._initialize_openai_engine()
        return QuestionIncorrectWorkflow(
            eval_switch,
            cls.get_database_engine(),
            cls.get_azure_openai_engine()
        )
        
    @classmethod
    def get_text_test_workflow(cls,eval_switch) -> TestWorkflow:
        logging.info("Creating TestWorkflow with dependencies")
        cls._initialize_openai_engine()
        return TestWorkflow(
            eval_switch,
            cls.get_database_engine(),
            cls.get_azure_openai_engine()
        )