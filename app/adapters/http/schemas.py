from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class WishCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    link: Optional[HttpUrl] = Field(None)
    price_estimate: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)


class WishUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    link: Optional[HttpUrl] = Field(None)
    price_estimate: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)
    is_purchased: Optional[bool] = None


class WishOut(WishCreate):
    id: int
    is_purchased: bool

    class Config:
        from_attributes = True  #
