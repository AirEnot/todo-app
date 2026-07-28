from unittest.mock import Mock

import pytest
from repositories.category import CategoryRepository
from repositories.task import TaskRepository
from services.category import CategoryService
from services.task import TaskService
from sqlalchemy.orm import Session


@pytest.fixture
def db_mock() -> Mock:
    return Mock(spec=Session)


@pytest.fixture
def task_repository_mock() -> Mock:
    return Mock(spec=TaskRepository)


@pytest.fixture
def task_service(db_mock: Mock, task_repository_mock: Mock) -> TaskService:
    service = TaskService(db_mock)
    service.task_repository = task_repository_mock
    return service


@pytest.fixture
def category_repository_mock() -> Mock:
    return Mock(spec=CategoryRepository)


@pytest.fixture
def category_service(db_mock: Mock, category_repository_mock: Mock) -> CategoryService:
    service = CategoryService(db_mock)
    service.category_repository = category_repository_mock
    return service
