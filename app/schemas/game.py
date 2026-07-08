from pydantic import BaseModel
class BookCreate(BaseModel):
    title: str
    author: str
    previe: int
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    previe: int