from sqlalchemy import ForeignKey, event, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from sqlalchemy.ext.hybrid import hybrid_property
from num2words import num2words

from src.db.models.brocker import Brocker
from src.db.models.contract import Contract
from .base import Base


class Photosession(Base):
    """Модель фотосессии в базе данных."""

    date: Mapped[str]
    url: Mapped[str]
    location: Mapped[str]
    price: Mapped[int]
    order: Mapped[int] = mapped_column(default=0)

    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contract.id", ondelete="CASCADE")
    )
    contract: Mapped["Contract"] = relationship(
        back_populates="photosessions",
        uselist=False,
        lazy="selectin"
    )
    brocker_id: Mapped[int] = mapped_column(
        ForeignKey("brocker.id", ondelete="CASCADE"),
        nullable=True
    )
    brocker: Mapped["Brocker"] = relationship(
        back_populates="photosessions",
        uselist=False,
        lazy="selectin"
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("service.id", ondelete="CASCADE")
    )
    service: Mapped["Service"] = relationship(
        back_populates="photosessions",
        uselist=False,
        lazy="selectin"
    )

    @hybrid_property
    def order_number(self) -> str:
        """Возвращает строковое представление порядкового номера фотосессии."""
        return f"{self.contract.name}-{self.order}"

    @hybrid_property
    def docx(self) -> str:
        """Возвращает имя файла документа для фотосессии."""
        return f"{self.order_number}.docx"

    @hybrid_property
    def price_litteral(self) -> str:
        """Возвращает строку с числительным для цены фотосессии."""
        return num2words(self.price, lang="ru")

    @hybrid_property
    def upper_order_number(self) -> str:
        """Возвращает порядковый номер фотосессии в верхнем регистре."""
        return f"{self.order_number.upper()}"


@event.listens_for(Photosession, 'before_insert')
def set_order(mapper: Mapper, connection, target):
    """Автоматически устанавливает порядковый номер фотосессии в рамках контракта."""
    if target.order is None or target.order == 0:
        result = connection.execute(
            select(func.max(Photosession.order))
            .where(Photosession.contract_id == target.contract_id)
        )
        max_order = result.scalar() or 0
        target.order = max_order + 1
