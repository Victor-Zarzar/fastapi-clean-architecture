from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    role: str
    disabled: bool


class UserOut(UserBase):
    id: int
    username: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: str
    disabled: bool = False

    model_config = ConfigDict(from_attributes=True)
