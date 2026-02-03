from pydantic import BaseModel, ConfigDict


class HealthCheckOut(BaseModel):
    status: str
    message: str
    details: str | None = None
    response_time: float

    model_config = ConfigDict(from_attributes=True)
