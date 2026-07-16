from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class GameCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    publisher: str = Field(min_length=1, max_length=40)
    short_description: str = Field(min_length=1, max_length=500)
    # category_id: int = Field(default=None)
    genre: str = Field(min_length=1, max_length=20)
    release_date: str = Field(min_length=1, max_length=40)
    thumbnail: Optional[str] = Field(min_length=1, max_length=500)


class GameUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    publisher: str | None = Field(default=None, min_length=1, max_length=40)
    short_description: str | None = Field(default=None, min_length=1, max_length=500)
    genre: str | None = Field(default=None)  # <--- ИСПРАВЛЕНО!
    release_date: str | None = Field(default=None, min_length=1, max_length=40)
    # category_id: int | None = Field(default=None, gt=0) 
    thumbnail: Optional[str] | None = Field(default=None, min_length=1, max_length=500)


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    publisher: str
    short_description: str
    genre: str
    release_date: str
    thumbnail: Optional[str]