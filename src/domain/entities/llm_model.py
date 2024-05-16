from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel, ForeignKey


if TYPE_CHECKING: pass
SCHEMA_NAME = "tagger"
metadata = MetaData(schema=SCHEMA_NAME)

class LLMModel(SQLModel, table=True): 
    llm_model_id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    description: str = Field(max_length=300, nullable=False) 
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, LLMModel):
            return False
        return (
            self.llm_model_id == other.llm_model_id
            and self.name == other.name
            and self.description == other.description
        )