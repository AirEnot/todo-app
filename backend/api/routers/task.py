from fastapi import APIRouter, Depends, status
from services.task import TaskService

from schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from api.dependecies import get_task_service


router = APIRouter(prefix='/tasks')

@router.get('', response_model=list[TaskSchema])
def get_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
   return task_service.list_tasks()


@router.post('', status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task( 
    payload: TaskCreateSchema,
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.create_task(payload)

@router.patch("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.update_task(task_id=task_id, task_to_update=payload)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service)
) -> None:
    task_service.delete_task(task_id=task_id)