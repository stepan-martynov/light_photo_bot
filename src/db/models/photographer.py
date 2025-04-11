from typing import List, Optional
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.db.models.user import User


class Photographer(User):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    inn: Mapped[int] = mapped_column(BigInteger)
    # kpp: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    ogrnip: Mapped[int] = mapped_column(BigInteger)
    address: Mapped[str]
    paymant_account: Mapped[str]
    opf_full: Mapped[str]
    opf_short: Mapped[str]

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

    # @hybrid_property
    # def opf_short(self) -> str:
    #     return f'{self.opf_full.split()[0][0]}{self.opf_full.split()[1][0].upper()}'
