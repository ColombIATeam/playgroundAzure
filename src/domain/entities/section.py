from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, MetaData, SQLModel


if TYPE_CHECKING: pass
SCHEMA_NAME = "tagger"
metadata = MetaData(schema=SCHEMA_NAME)

class Section(SQLModel, table=True):
    section_id: Optional[int] = Field(primary_key=True)
    section_name: str
    content: str = ""
    topic_id: int = Field(foreign_key="topic.topic_id")
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, Section):
            return False
        return (
            self.section_id == other.section_id
            and self.section_name == other.section_name
            and self.content == other.content
            and self.topic_id == other.topic_id
        )