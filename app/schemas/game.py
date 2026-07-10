from pydantic import BaseModel, ConfigDict, Field
from app.schemas.cat import CatResponse  


class GameCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=200)
    prev: str = Field(min_length=1, max_length=200)
    category_id: int = Field(gt=0)

class GameUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=200)
    prev: str | None = Field(default=None, min_length=1, max_length=200)


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    prev: str
    category: CatResponse | None = None 
