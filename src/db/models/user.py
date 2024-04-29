from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property


class User(Base):
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    tel: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]

    role: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "role"
    }

    @hybrid_property
    def full_name(self) -> str:
        return f'{self.last_name} {self.name} {self.patronymic}'

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.full_name!r}, tel={self.tel!r})'
