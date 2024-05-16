from typing import List
from pydantic import BaseModel

class QuestionIncorrectRequest(BaseModel):
    Enunciado: str
    Respuesta_correcta: str
    razonamiento_correcto: str

class ListQuestionIncorrectRequest(BaseModel):
    Questions: List[QuestionIncorrectRequest]
    prompt: str