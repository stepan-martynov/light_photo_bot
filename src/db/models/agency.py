from sqlalchemy.orm import Mapped

from .base import Base
from .manager import Manager
from .bank_accaunt import BankAccaunt

class Agency(Base):
    name: Mapped[str]
    inn: Mapped[int]
    kpp: Mapped[int]
    ogrn: Mapped[str]
    opf: Mapped[str]
    opf_full: Mapped[str]
    opf_short: Mapped[str]
    address: Mapped[str]
    manager: Mapped[Manager]
    bank_accaunt: Mapped[BankAccaunt]
    