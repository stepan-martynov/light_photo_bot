from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .base import Base
from num2words import num2words


class Photosession(Base):
    date: Mapped[str]
    url: Mapped[str]
    address: Mapped[str]

    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.id", ondelete="CASCADE"))
    contract: Mapped["Contract"] = relationship(back_populates="photosessions", uselist=False, lazy="selectin")

    @hybrid_property
    def order(self) -> str:
        return f"{self.contract.name}-{self.id}"

    @hybrid_property
    def docx(self) -> str:
        return f"{self.order}.docx"

    @hybrid_property
    def price_in_words(self) -> str:
        words = num2words(self.price, lang="ru")
        return f"{words}"
