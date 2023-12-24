from typing import List
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Brocker(Base):
    telegram_id: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped

    protosessions: Mapped[List["Photosession"]] = relationship(back_populates="brocker", uselist=True)
