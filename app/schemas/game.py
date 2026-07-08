from pydantic import BaseModel

class GameCreate(BaseModel):
    title: str
    author: str
    previe: str

class GameResponse(BaseModel):
    id: int
    title: str
    author: str
    previe: str
