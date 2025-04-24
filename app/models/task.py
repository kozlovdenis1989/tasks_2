from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, func
from ..repository.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    due_date = Column(TIMESTAMP, nullable=True)
    status = Column(Boolean, default=False, nullable=False)