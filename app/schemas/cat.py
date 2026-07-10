from pydantic import BaseModel, ConfigDict, Field


class CatCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class CatUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)


class CatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

