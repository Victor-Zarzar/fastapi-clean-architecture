from pydantic import BaseModel


class KafkaMessage(BaseModel):
    key: str
    value: str


class KafkaPublishResponse(BaseModel):
    sent: bool
    payload: KafkaMessage
    user: str
