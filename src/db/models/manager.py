from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Manager(Base):
    full_name: Mapped[str]
    post: Mapped[str]

    agency_id: Mapped[int] = mapped_column(ForeignKey("agency.id", ondelete="CASCADE"))
    agency: Mapped["Agency"] = relationship(back_populates="manager")

    @hybrid_property
    def second_name(self) -> str:
        return self.full_name.split()[0]
    
    @hybrid_property
    def initials(self) -> str:
        return f'{self.full_name.split()[1][0]}. {self.full_name.split()[2][0]}.'
