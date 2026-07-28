from exeptions.category import CategoryNotFoundError
from repositories.category import CategoryRepository
from schemas.category import CategoryCreateSchema, CategorySchema, CategoryUdpateSchema
from sqlalchemy.orm import Session


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_all(self) -> list[CategorySchema]:
        categories = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories]

    def create_category(
        self, categoty_to_create: CategoryCreateSchema
    ) -> CategorySchema:
        category_orm = self.category_repository.create(categoty_to_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(
        self, id: str, category_update: CategoryUdpateSchema
    ) -> CategorySchema:
        category_orm = self.category_repository.get_by_id(id=id)

        if category_orm is None:
            raise CategoryNotFoundError(f"Категория {id} не найдена")

        category_orm.name = category_update.name
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def delete_category(self, id: str) -> None:
        category_orm = self.category_repository.get_by_id(id)

        if category_orm is None:
            raise CategoryNotFoundError(f"Категория {id} не найдена")

        self.db.delete(category_orm)
        self.db.commit()
