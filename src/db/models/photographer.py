from typing import List
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.db.models.user import User


class Photographer(User):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    inn: Mapped[int] = mapped_column(BigInteger)
    # kpp: Mapped[int] = mapped_column(BigInteger)
    # address: Mapped[str]
    paymant_account: Mapped[str]

    contracts: Mapped[List["Contract"]] = relationship(back_populates="photographer", uselist=True)
    services: Mapped[List["Service"]] = relationship(back_populates="photographer", uselist=True)
    bank_accaunt_id: Mapped[int] = mapped_column(ForeignKey("bank_accaunt.id", ondelete="CASCADE"))
    bank_accaunt: Mapped["BankAccaunt"] = relationship(back_populates="photographers", uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "photographer",
    }

    @hybrid_property
    def initials(self) -> str:
        return f'{self.last_name} {self.name[0]}. {self.patronymic[0]}.'
