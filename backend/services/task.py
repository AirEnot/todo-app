from repositories.task import TaskReposytory
from schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from sqlalchemy.orm import Session


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskReposytory(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_to_update: TaskUpdateSchema) -> TaskSchema:
        task_orm = self.task_repository.get_by_id(task_id=task_id)

        if task_to_update.title is not None:
            task_orm.title = task_to_update.title

        if task_to_update.completed is not None:
            task_orm.completed = task_to_update.completed

        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def delete_task(self, task_id: str) -> None:
        task_orm = self.task_repository.get_by_id(task_id=task_id)
        self.task_repository.delete(task=task_orm)
        self.db.commit()
