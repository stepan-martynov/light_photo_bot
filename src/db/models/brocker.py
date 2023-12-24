from typing import List

from sqlalchemy import ForeignKey
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Brocker(Base):
    telegram_id: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped

    protosessions: Mapped[List["Photosession"]] = relationship(back_populates="brocker", uselist=True, lazy="selectin")
    agency_id: Mapped[int] = mapped_column(ForeignKey("agency.id", ondelete="CASCADE"))
    agency: Mapped["Agency"] = relationship(back_populates="brockers", uselist=False, lazy="selectin")
