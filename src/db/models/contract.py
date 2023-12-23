from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base

class Contract(Base):
    date: Mapped[str]

    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer.id", ondelete="CASCADE"))
    photographer: Mapped["Photographer"] = relationship(back_populates="contracts", uselist=False)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agency.id", ondelete="CASCADE"))
    agency: Mapped["Agency"] = relationship(back_populates="contracts", uselist=False)
    photosessions: Mapped[List["Photosession"]] = relationship(back_populates="contract", uselist=True, lazy="selectin")

    @hybrid_property
    def name(self) -> str:
        return f"{self.photographer.last_name[0]}{self.agency.name[0]}-{self.date}"

    @hybrid_property
    def docx(self) -> str:
        return f"{self.name}.docx"
