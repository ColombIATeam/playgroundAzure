from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel, ForeignKey


if TYPE_CHECKING: pass
SCHEMA_NAME = "tagger"
metadata = MetaData(schema=SCHEMA_NAME)

class Prompt(SQLModel, table=True):  
    prompt_id: Optional[int] = Field(default=None, primary_key=True, nullable=False)  
    category: str = Field(max_length=300, nullable=False)  
    name: str = Field(max_length=100, nullable=False)  
    description: str = Field(max_length=300, nullable=False)  
    system_message: str = Field(nullable=False)  
    llm_model_id: int = Field(ForeignKey("llm_model.llm_model_id"), nullable=False)  
    max_response_length: int = Field(nullable=False)  
    temperature: float = Field(nullable=False)  
    top_probabilities: float = Field(nullable=False)  
    stop_sequences: str = Field(nullable=True)  
    frequency_penalty: float = Field(nullable=False)  
    presence_penalty: float = Field(nullable=False)  
    stream: bool = Field(nullable=False)
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, Prompt):
            return False
        return (
            self.prompt_id == other.prompt_id
            and self.name == other.name
            and self.description == other.description
            and self.llm_model_id == other.llm_model_id
        )
        