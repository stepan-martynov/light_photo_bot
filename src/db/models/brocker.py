from typing import List

from sqlalchemy import ForeignKey

from src.db.models.user import User
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Brocker(User):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    photosessions: Mapped[List["Photosession"]] = relationship(back_populates="brocker", uselist=True)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agency.id", ondelete="CASCADE"), nullable=True)
    agency: Mapped["Agency"] = relationship(back_populates="brockers", uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "brocker",
    }
