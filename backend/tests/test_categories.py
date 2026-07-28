from unittest.mock import Mock

import pytest
from exeptions.category import CategoryNotFoundError
from models.category import CategoryORM
from schemas.category import CategoryCreateSchema, CategorySchema, CategoryUdpateSchema
from services.category import CategoryService


def test_list_all_categories(
    category_service: CategoryService, category_repository_mock: Mock
) -> None:
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="1", name="Категория слоны"),
        CategoryORM(id="2", name="Пупупу"),
    ]

    result = category_service.get_all()

    assert result == [
        CategorySchema(id="1", name="Категория слоны"),
        CategorySchema(id="2", name="Пупупу"),
    ]


def test_category_service_returns_valid_schema(
    category_service: CategoryService, category_repository_mock: Mock, db_mock: Mock
) -> None:
    category_repository_mock.create.return_value = CategoryORM(
        id="1", name="Новая категория"
    )

    result = category_service.create_category(
        CategoryCreateSchema(name="Новая категория")
    )

    category_repository_mock.create.assert_called_once()
    db_mock.commit.assert_called_once()

    assert result == CategorySchema(id="1", name="Новая категория")


def test_catrgory_udpate_returns_correct_model(
    category_service: CategoryService, category_repository_mock: Mock, db_mock: Mock
) -> None:
    category_orm = CategoryORM(id="23", name="Измененное название")
    category_repository_mock.get_by_id.return_value = category_orm

    result = category_service.update_category(
        id="23", category_update=CategoryUdpateSchema(name="Измененное название")
    )

    category_repository_mock.get_by_id.assert_called_once_with(id="23")
    db_mock.commit.assert_called_once()

    assert result == CategorySchema(id="23", name="Измененное название")


def test_category_delete_raises_not_found_error(
    category_repository_mock: Mock, category_service: CategoryService, db_mock: Mock
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        category_service.delete_category(id="111")

    db_mock.delete.assert_not_called()
    db_mock.commit.assert_not_called()
