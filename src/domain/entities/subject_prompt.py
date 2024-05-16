from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel, ForeignKey


if TYPE_CHECKING: pass
SCHEMA_NAME = "tagger"
metadata = MetaData(schema=SCHEMA_NAME)

class Subject_Prompt(SQLModel, table=True):   
    prompt_subject_id: Optional[int] = Field(default=None, primary_key=True, nullable=False)  
    subject_id: Optional[int] = Field(ForeignKey("subject.subject_id"), nullable=False)
    prompt_id: Optional[int] = Field(ForeignKey("prompt.prompt_id"), nullable=False)  
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, Subject_Prompt):
            return False
        return (
            self.prompt_subject_id == other.prompt_subject_id
            and self.subject_id == other.subject_id
            and self.prompt_id == other.prompt_id
        )