from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from schemas import *



app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

tasks: list[TaskSchema] = []


@app.get('/tasks')
def get_tasks():
    return tasks


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
        
            return task
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return 
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


categories: list[CategorySchema] = []

@app.get('/categories', response_model=list[CategorySchema])
def get_catrgories():
    return categories

@app.post('/categories', response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema):
    category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(category)
    return category

@app.patch('/categories/{category_id}', response_model=CategorySchema)
def update_category(category_id: str, payload: CategoryUdpateSchema):
    for category in categories:
        if category.id == category_id:
            category.name = payload.name
            return category
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')

@app.delete('/categories/{category_id}')
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return category

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Не найдена категория: {category_id}')