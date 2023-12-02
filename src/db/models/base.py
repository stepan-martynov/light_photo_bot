from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

@as_declarative()
class Base:

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)