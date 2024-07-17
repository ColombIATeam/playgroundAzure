import sys
from api.workflows.test_questions.test_workflow import TestWorkflow
from api.workflows.question_correct.question_correct_workflow import QuestionCorrectWorkflow
from api.workflows.question_incorrect.question_incorrect_workflow import QuestionIncorrectWorkflow
from common.application_settings import ApplicationSettings
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import create_async_engine
import logging


class DependencyContainer:
    _application_settings: ApplicationSettings
    _database_engine: Engine

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
    def _initialize_database_engine(cls) -> None:
        url = f"mssql+aioodbc://{cls._application_settings.SQL_SERVER__USERNAME}:{cls._application_settings.SQL_SERVER__PASSWORD}@{cls._application_settings.SQL_SERVER__HOST}:{cls._application_settings.SQL_SERVER__PORT}/{cls._application_settings.SQL_SERVER__NAME}?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
        cls._database_engine = create_async_engine(url=url, echo=False)  

    @classmethod
    def get_question_correct_workflow(cls,eval_switch) -> QuestionCorrectWorkflow:
        logging.info("Creating QuestionCorrectWorkflow with dependencies")
        return QuestionCorrectWorkflow(
            eval_switch,
            cls.get_database_engine()
        )
    
    @classmethod
    def get_question_incorrect_workflow(cls,eval_switch) -> QuestionIncorrectWorkflow:
        logging.info("Creating QuestionIncorrectWorkflow with dependencies")
        return QuestionIncorrectWorkflow(
            eval_switch,
            cls.get_database_engine()
        )
        
    @classmethod
    def get_text_test_workflow(cls,eval_switch) -> TestWorkflow:
        logging.info("Creating TestWorkflow with dependencies")
        return TestWorkflow(
            eval_switch,
            cls.get_database_engine()
        )