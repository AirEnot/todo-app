from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, mapped_column, DeclarativeBase, sessionmaker, Mapped


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "task"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

tasks: list[TaskSchema] = []


def task_orm_to_schema(task: TaskORM) -> TaskSchema:
    return TaskSchema(id=task.id, title=task.title, completed=task.completed)


@app.get('/tasks', response_model=list[TaskSchema])
def get_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_schema(task) for task in tasks_from_db]


@app.post('/tasks', status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task = TaskORM(title=payload.title, completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_orm_to_schema(task)



@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    # task = db.scalar(select(TaskORM).where(TaskORM.id==task_id))
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    
    task.title = payload.title if payload.title is not None else task.title
    task.completed = payload.completed if payload.completed is not None else task.completed
    db.commit()
    db.refresh(task)
    return task_orm_to_schema(task)


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    db.delete(task)
    db.commit()


# -----------------------------------------------------------------------------------------------------------------
# categories: list[CategorySchema] = []

class CategoryORM(Base):
    __tablename__ = "category"
    name: Mapped[str] 

def category_orm_to_schema(category: CategoryORM):
    return CategorySchema(id=category.id, name=category.name)


@app.get('/categories', response_model=list[CategorySchema])
def get_catrgories(db: Session = Depends(get_db)):
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_schema(cat) for cat in categories_from_db]

@app.post('/categories', response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, db: Session = Depends(get_db)):
    category = CategoryORM(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category_orm_to_schema(category)


@app.patch('/categories/{category_id}', response_model=CategorySchema)
def update_category(category_id: str, payload: CategoryUdpateSchema, db: Session = Depends(get_db)):
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')
    
    category.name = payload.name
    db.commit()
    db.refresh(category)

    return category_orm_to_schema(category)    

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')
    
    db.delete(category)
    db.commit()
    