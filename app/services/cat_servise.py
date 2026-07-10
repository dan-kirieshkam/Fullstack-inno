from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cat import Cat
from app.repositories.cat_repository import CatRepository
from app.schemas.cat import CatCreate, CatUpdate


class CatService:

    def __init__(self, db: Session):
        self.repository = CatRepository(db)

    def create_cat(self, schema: CatCreate) -> Cat:
        cat = Cat(
            name=schema.name,
        )

        return self.repository.create(cat)

    def get_cats(self) -> list[Cat]:
        return self.repository.get_all()

    def get_cat(self, cat_id: int) -> Cat:
        cat = self.repository.get_by_id(cat_id)

        if cat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return cat
    def update_cat(
        self,
        cat_id: int,
        schema: CatUpdate,
    ) -> Cat:

        cat = self.get_cat(cat_id)

        if schema.name is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.name is not None:
            cat.name = schema.name


        return self.repository.update(cat)

    def delete_cat(self, cat_id: int) -> None:
        cat = self.get_cat(cat_id)

        self.repository.delete(cat)