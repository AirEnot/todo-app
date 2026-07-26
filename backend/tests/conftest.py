from unittest.mock import Mock

import pytest
from repositories.task import TaskRepository
from services.task import TaskService
from sqlalchemy.orm import Session


@pytest.fixture
def db_mock() -> Mock:
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    task_service = TaskService(db_mock)
    task_service.task_repository = repository_mock  # pyright: ignore
    return task_service
