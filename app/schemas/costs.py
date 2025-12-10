from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CostOfLivingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3, default="BRL")
    city: Optional[str] = Field(default=None, max_length=120)
    country: Optional[str] = Field(default=None, max_length=120)


class CostOfLiving(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: Optional[str] = None
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    currency: str
    city: Optional[str] = None
    country: Optional[str] = None


class CostOfLivingUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)
    amount: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)
    city: Optional[str] = Field(default=None, max_length=120)
    country: Optional[str] = Field(default=None, max_length=120)
