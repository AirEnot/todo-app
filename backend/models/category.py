from models.base import Base
from sqlalchemy.orm import Mapped

class CategoryORM(Base):
    __tablename__ = "category"
    name: Mapped[str] 