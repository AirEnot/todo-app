from unittest.mock import Mock

import pytest
from exeptions.task import TaskNotFoundError
from models.task import TaskORM
from schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from services.task import TaskService


def test_list_tasks_returns_pydantic_models(
    task_service: TaskService, task_repository_mock: Mock
) -> None:
    task_repository_mock.get_all.return_value = [
        TaskORM(id="1", title="Задача 1", completed=False),
        TaskORM(id="2", title="Задача 2", completed=True),
    ]

    result = task_service.list_tasks()

    assert result == [
        TaskSchema(id="1", title="Задача 1", completed=False),
        TaskSchema(id="2", title="Задача 2", completed=True),
    ]


def test_servise_create_task(
    task_service: TaskService, task_repository_mock: Mock, db_mock: Mock
) -> None:
    created_task = TaskCreateSchema(title="Новая задача")
    task_repository_mock.create.return_value = TaskORM(
        id="1", title="Новая задача", completed=False
    )

    result = task_service.create_task(created_task)

    task_repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once()

    assert result == TaskSchema(
        id="1",
        title="Новая задача",
        completed=False,
    )


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(TaskUpdateSchema(title="Новая задача"), "Новая задача", False),
        pytest.param(TaskUpdateSchema(completed=True), "Задача", True),
        pytest.param(
            TaskUpdateSchema(title="Новая задача", completed=True), "Новая задача", True
        ),
    ],
)
def test_update_task_updates_only_passed_fields(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
    payload: TaskUpdateSchema,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(id="1", title="Задача", completed=False)
    task_repository_mock.get_by_id.return_value = task

    result = task_service.update_task(task_id="1", task_to_update=payload)

    task_repository_mock.get_by_id.assert_called_once_with(task_id="1")
    db_mock.commit.assert_called_once()

    assert result == TaskSchema(
        id="1", title=expected_title, completed=expected_completed
    )


def test_update_task_raises_task_not_found_error(
    task_service: TaskService, db_mock: Mock, task_repository_mock: Mock
) -> None:
    task_repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):
        task_service.update_task(
            task_id="1", task_to_update=TaskUpdateSchema(title="Unknown task")
        )

    db_mock.commit.assert_not_called()
