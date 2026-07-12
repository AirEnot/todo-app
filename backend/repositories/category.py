from sqlalchemy.orm import Session
from sqlalchemy import select 
from models.category import CategoryORM


class CategoryRepository:
    def __init__ (self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())
    
    def get_by_id(self, id: str) -> CategoryORM:
        category = self.db.get(CategoryORM, id)
        if category is None: 
            raise ValueError(f"Task {id} not found")
        return category
    def create(self, name: str) -> CategoryORM:
        category = CategoryORM(name=name)
        self.db.add(category)
        return category
    
    def delete(self, category_id: str) -> None:
        category = self.get_by_id(category_id) 
        self.db.delete(category)