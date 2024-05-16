from pydantic import BaseModel
from typing import List


class QuestionIncorrectResponse(BaseModel):
    incorrect_answers: dict

class ListQuestionIncorrectResponse(BaseModel):
    incorrect_answer_list: List[QuestionIncorrectResponse]
    prompt_improving: str