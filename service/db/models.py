from sqlalchemy import Column, DateTime, Integer, MetaData, Text
from sqlalchemy.orm import declarative_base

metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)


class Documents(DeclarativeBase):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rubrics = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    created_date = Column(DateTime(), nullable=False)
