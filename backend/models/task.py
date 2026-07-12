from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class TaskORM(Base):
    __tablename__ = "task"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
