from sqlalchemy.orm import mapped_column, Mapped
from src.models import Base


class City(Base):
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(unique=True)
    additional_info: Mapped[str | None]

    def __repr__(self) -> str:
        return self.name
