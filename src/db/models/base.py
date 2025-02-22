import re
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

@as_declarative()
class Base:

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
