from pydantic import BaseModel
from typing import List


class QuestionCorrectResponse(BaseModel):
    enunciado: str
    respuesta_correcta: str
    razonamiento_correcto: str


class ListQuestionCorrectResponse(BaseModel):
    correct_answer_list: List[QuestionCorrectResponse]
    prompt_improving: str