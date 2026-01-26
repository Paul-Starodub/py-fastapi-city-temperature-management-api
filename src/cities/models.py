from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.models import Base

if TYPE_CHECKING:
    from src.temperatures.models import Temperature


class City(Base):
    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(unique=True)
    additional_info: Mapped[str | None]
    temperatures: Mapped[list["Temperature"]] = relationship(back_populates="city")

    def __repr__(self) -> str:
        return self.name
