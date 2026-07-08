from pydantic import BaseModel
<<<<<<< HEAD
class BookCreate(BaseModel):
    title: str
    author: str
    previe: int
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    previe: int
=======

class GameCreate(BaseModel):
    title: str
    author: str
    previe: str

class GameResponse(BaseModel):
    id: int
    title: str
    author: str
    previe: str
>>>>>>> a612e787b71ad0443df6cf4cac1d699371ab7049
