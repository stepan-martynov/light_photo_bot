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


    manager: Mapped["Manager"] = relationship(back_populates="agency")
    bank_accaunt: Mapped["BankAccaunt"] = relationship(back_populates="agency")
