from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel, ForeignKey


if TYPE_CHECKING: pass
SCHEMA_NAME = "tagger"
metadata = MetaData(schema=SCHEMA_NAME)

class Summary(SQLModel, table=True):
    summary_id: Optional[int] = Field(default=None, primary_key=True)
    summary: str
    section_id: int = Field(foreign_key="section.section_id")
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, Summary):
            return False
        return (
            self.summary_id == other.summary_id
            and self.summary == other.summary
            and self.section_id == other.section_id
        )