from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base


class BankAccaunt(Base):
    name: Mapped[str]
    bik: Mapped[int]
    paymant_account: Mapped[str]
    cor_account: Mapped[str]

    agency_id: Mapped[int] = mapped_column(ForeignKey("agency.id", ondelete="CASCADE"))
    agency: Mapped["Agency"] = relationship(back_populates="bank_accaunt")
