from sqlalchemy.orm import Session

from app.models.cat import Cat


class CatRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, cat: Cat) -> Cat:
        return self._upsert(cat)

    def update(self, cat: Cat) -> Cat:
        return self._upsert(cat)

    def _upsert(self, cat: Cat) -> Cat:
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)

        return cat

    def get_all(self) -> list[Cat]:
        return self.db.query(Cat).all()

    def get_by_id(
        self,
        cat_id: int,
    ) -> Cat | None:

        return (
            self.db.query(Cat)
            .filter(Cat.id == cat_id)
            .first()
        )

    def delete(self, cat: Cat) -> None:
        self.db.delete(cat)
        self.db.commit()