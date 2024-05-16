from api.workflows.question_correct.question_correct_request import QuestionCorrectRequest
from api.workflows.question_correct.question_correct_response import ListQuestionCorrectResponse
from api.workflows.question_incorrect.question_incorrect_request import QuestionIncorrectRequest
from api.workflows.question_incorrect.question_incorrect_response import ListQuestionIncorrectResponse
from api.workflows.test_questions.test_request import TestRequest
from api.workflows.test_questions.test_response import GenerarTestsResponse
from api.common.dependency_container import DependencyContainer
from fastapi import APIRouter


router = APIRouter(prefix="/question", tags=["questions"])


@router.post("/generate_question/")
def text_test(request:TestRequest)->GenerarTestsResponse:
    return DependencyContainer.get_text_test_workflow().execute(request)

@router.post("/question_correct/")
def question_correct(request: QuestionCorrectRequest) -> ListQuestionCorrectResponse:
    return DependencyContainer.get_question_correct_workflow().execute(request)

@router.post("/question_incorrect/")
def question_incorrect(request: QuestionIncorrectRequest) -> ListQuestionIncorrectResponse:
    return DependencyContainer.get_question_incorrect_workflow().execute(request)

