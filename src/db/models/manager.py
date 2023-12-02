from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped

from .base import Base


class Manager(Base):
    full_name: Mapped[str]
    post: Mapped[str]

    @hybrid_property
    def second_name(self) -> str:
        return self.full_name.split()[0]
    
    @hybrid_property
    def initials(self) -> str:
        return f'{self.full_name.split()[1][0]}. {self.full_name.split()[2][0]}.'
