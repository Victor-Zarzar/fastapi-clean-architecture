from pydantic import BaseModel


class KafkaMessage(BaseModel):
    key: str
    value: str
