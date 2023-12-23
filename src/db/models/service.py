from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Service(Base):
    name: Mapped[str]
    price: Mapped[int]

    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer.id", ondelete="CASCADE"))
    photographer: Mapped["Photographer"] = relationship(back_populates="services", uselist=False)
