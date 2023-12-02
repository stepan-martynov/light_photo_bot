from sqlalchemy.orm import Mapped

from .base import Base


class Manager(Base):
    full_name: Mapped[str]
    post: Mapped[str]

    @property
    def second_name(self) -> str:
        return self.full_name.split()[0]
    
    @property
    def initial(self) -> str:
        return f'{self.full_name.split()[1][0]}. {self.full_name.split()[2][0]}.'
