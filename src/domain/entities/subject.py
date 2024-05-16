from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel, ForeignKey


schema_name = 'tagger'
metadata = MetaData(schema=schema_name)

class Subject(SQLModel, table=True):
    subject_id: Optional[int] = Field(default=None, primary_key=True)
    subject_name: str
    description: str
    study_id: Optional[int] = Field(default=None, primary_key=True)
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, Subject):
            return False
        return (
            self.subject_id == other.subject_id
            and self.subject_name == other.subject_name
            and self.description == other.description
            and self.study_id == other.study_id
        )