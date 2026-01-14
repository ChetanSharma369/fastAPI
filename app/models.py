from .databases import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = 'details'

    id=Column(Integer, primary_key=True, nullable=False)
    name=Column(String, nullable=False)
    city=Column(String,nullable=False)
    published=Column(Boolean, server_default='FALSE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


