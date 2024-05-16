from typing import List
from pydantic import BaseModel

class QuestionCorrectRequest(BaseModel):
    Enunciado: str
    Razonamiento: str

class ListQuestionCorrectRequest(BaseModel):
    Questions: List[QuestionCorrectRequest]
    prompt_table: str