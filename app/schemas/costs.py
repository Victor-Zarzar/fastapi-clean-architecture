from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CostOfLivingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3, default="BRL")
    city: str | None = Field(default=None, max_length=120)
    country: str | None = Field(default=None, max_length=120)


class CostOfLiving(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str | None = None
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    currency: str
    city: str | None = None
    country: str | None = None


class CostOfLivingUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    amount: Decimal | None = Field(default=None, max_digits=12, decimal_places=2)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    city: str | None = Field(default=None, max_length=120)
    country: str | None = Field(default=None, max_length=120)
