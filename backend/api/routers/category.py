from fastapi import APIRouter, Depends, status
from schemas.category import CategoryCreateSchema, CategorySchema, CategoryUdpateSchema
from services.category import CategoryService

from api.dependecies import get_category_service

router = APIRouter(prefix="/categories")


@router.get("", response_model=list[CategorySchema])
def get_catrgories(category_service: CategoryService = Depends(get_category_service)):
    return category_service.get_all()


@router.post("", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.create_category(payload)


@router.patch("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: str,
    payload: CategoryUdpateSchema,
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.update_categoty(id=category_id, category_update=payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str, category_service: CategoryService = Depends(get_category_service)
):
    category_service.delete_category(id=category_id)
