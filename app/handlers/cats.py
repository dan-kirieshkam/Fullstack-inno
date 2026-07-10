from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cat import CatCreate, CatResponse, CatUpdate
from app.services.cat_servise import CatService

router = APIRouter(
    prefix="/catigories",
    tags=["catigories"],
)


def get_cat_service(
    db: Session = Depends(get_db),
) -> CatService:
    return CatService(db)


@router.post(
    "/",
    response_model=CatResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cat(
    schema: CatCreate,
    service: CatService = Depends(get_cat_service),
):
    return service.create_cat(schema)


@router.get(
    "/",
    response_model=list[CatResponse],
)
def get_cats(
    service: CatService = Depends(get_cat_service),
):
    return service.get_cats()


@router.get(
    "/{cat_id}",
    response_model=CatResponse,
)
def get_cat(
    cat_id: int,
    service: CatService = Depends(get_cat_service),
):
    return service.get_cat(cat_id)


@router.patch(
    "/{cat_id}",
    response_model=CatResponse,
)
def update_cat(
    cat_id: int,
    schema: CatUpdate,
    service: CatService = Depends(get_cat_service),
):
    return service.update_cat(cat_id, schema)


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_cat(
    cat_id: int,
    service: CatService = Depends(get_cat_service),
) -> None:
    service.delete_cat(cat_id)