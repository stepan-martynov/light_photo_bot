from typing import List
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Service(Base):
    name: Mapped[str]
    default_price: Mapped[int]

    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer.id", ondelete="CASCADE"))
    photographer: Mapped["Photographer"] = relationship(back_populates="services", uselist=False)

    photosessions: Mapped[List["Photosession"]] = relationship(back_populates="service", uselist=True, lazy="selectin")
