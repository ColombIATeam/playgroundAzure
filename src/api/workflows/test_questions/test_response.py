from typing import List
from pydantic import BaseModel


class TestQuestion(BaseModel):
    Enunciado: str
    Razonamiento: str


class GenerarTestsResponse(BaseModel):
    test: List[TestQuestion]
    prompt_improving: str