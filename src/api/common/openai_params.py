from pydantic import BaseModel


class OpenaiParams(BaseModel):
    deployment_name: str
    max_response_length: int
    temperature: float
    top_probablities: float
    stop_sequences: str | None
    past_messages_to_include: int | None
    frequency_penalty: float | None
    presence_penalty: float | None