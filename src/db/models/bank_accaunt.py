from sqlalchemy.orm import Mapped

from .base import Base


class BankAccaunt(Base):
    name: Mapped[str]
    bik: Mapped[int]
    paymant_account: Mapped[str]
    cor_account: Mapped[str]

