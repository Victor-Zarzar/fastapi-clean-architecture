from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=255)
    role: str = "basic"
    disabled: bool = False
    email_verified: bool = False


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
