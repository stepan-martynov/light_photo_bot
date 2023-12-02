from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Agency(Base):
    name: Mapped[str]
    inn: Mapped[int]
    kpp: Mapped[int]
    ogrn: Mapped[str]
    opf_full: Mapped[str]
    opf_short: Mapped[str]
    address: Mapped[str]

    manager: Mapped["Manager"] = relationship(back_populates="agency")
    bank_accaunt: Mapped["BankAccaunt"] = relationship(back_populates="agency")
    