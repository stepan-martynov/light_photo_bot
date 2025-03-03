from typing import List
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Agency(Base):
    name: Mapped[str]
    inn: Mapped[int] = mapped_column(BigInteger)
    kpp: Mapped[int] = mapped_column(BigInteger)
    ogrn: Mapped[int] = mapped_column(BigInteger)
    opf_full: Mapped[str]
    opf_short: Mapped[str]
    opf_full: Mapped[str]
    address: Mapped[str]
    paymant_account: Mapped[str]

    manager: Mapped["Manager"] = relationship(back_populates="agency", uselist=False)
    contracts: Mapped[List["Contract"]] = relationship(back_populates="agency", uselist=True, lazy=True)
    bank_accaunt_id: Mapped[int] = mapped_column(ForeignKey("bank_accaunt.id", ondelete="CASCADE"))
    bank_accaunt: Mapped["BankAccaunt"] = relationship(back_populates="agencies", uselist=False)
    brockers: Mapped[List["Brocker"]] = relationship(back_populates="agency", uselist=True)

    def __str__(self):
        return f"<{self.name=} ({self.inn=})>"

    def __repr__(self) -> str:
        return f'Agency(id={self.id!r}, name={self.name!r}, inn={self.inn!r}), bank_accaunt_id={self.bank_accaunt_id!r})'
