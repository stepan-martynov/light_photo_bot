from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey

from .base import Base


class BankAccaunt(Base):
    name: Mapped[str]
    bic: Mapped[str]
    correspondent_account: Mapped[str]
    address: Mapped[str]

    agencies: Mapped[List["Agency"]] = relationship(back_populates="bank_accaunt", uselist=True)
    photographers: Mapped[List["Photographer"]] = relationship(back_populates="bank_accaunt", uselist=True)
