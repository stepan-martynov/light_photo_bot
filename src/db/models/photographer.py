from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base


class Photographer(Base):
    teegram_id: Mapped[str]
    name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]
    chat_id: Mapped[str]
    tel: Mapped[str]
    inn: Mapped[int]
    payment_account: Mapped[str]

    contracts: Mapped[List["Contract"]] = relationship(back_populates="photographer", uselist=True)
    services: Mapped[List["Service"]] = relationship(back_populates="photographer", uselist=True)
    bank_accaunt_id: Mapped[int] = mapped_column(ForeignKey("bank_accaunt.id", ondelete="CASCADE"))
    bank_accaunt: Mapped["BankAccaunt"] = relationship(back_populates="photographers", uselist=False)

    @hybrid_property
    def initials(self) -> str:
        return f'{self.last_name} {self.name[0]}. {self.patronymic[0]}.'
