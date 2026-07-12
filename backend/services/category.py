from sqlalchemy.orm import Session

from repositories.category import CategoryRepository
from schemas.category import CategoryCreateSchema, CategorySchema, CategoryUdpateSchema


class CategoryService:
    def __init__ (self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_all(self) -> list[CategorySchema]:
        categories = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories]

    def create_category(self, categoty_to_create: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repository.create(categoty_to_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)
    
    def update_categoty(
            self, 
            id: str, 
            category_update: CategoryUdpateSchema
        ) -> CategorySchema:
        category_orm = self.category_repository.get_by_id(id=id)
        
        category_orm.name = category_update.name
        self.db.commit()
        return CategorySchema.model_validate(category_orm)
    
    def delete_category(self, id: str) -> None:
        category_orm = self.category_repository.get_by_id(id)
        self.db.delete(category_orm)
        self.db.commit()
