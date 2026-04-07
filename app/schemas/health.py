from pydantic import BaseModel


class HealthCheckOut(BaseModel):
    status: str
    message: str
    details: str
    response_time: float
