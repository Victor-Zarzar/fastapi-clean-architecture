from typing import Optional

from pydantic import BaseModel, ConfigDict


class HealthCheckOut(BaseModel):
    status: str
    message: str
    details: Optional[str] = None
    response_time: float

    model_config = ConfigDict(from_attributes=True)
