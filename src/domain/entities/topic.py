from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel, ForeignKey


if TYPE_CHECKING: pass
SCHEMA_NAME = "tagger"
metadata = MetaData(schema=SCHEMA_NAME)

class Topic(SQLModel, table=True):
    topic_id: Optional[int] = Field(default=None, primary_key=True)
    topic_name: str
    topic_version: Optional[str]
    description: Optional[str] = None
    subject_id: Optional[int] = Field(foreign_key="subject.subject_id")
    metadata = metadata
    def __eq__(self, other):
        if not isinstance(other, Topic):
            return False
        return (
            self.topic_id == other.topic_id
            and self.topic_name == other.topic_name
            and self.topic_version == other.topic_version
            and self.description == other.description
            and self.subject_id == other.subject_id
        )