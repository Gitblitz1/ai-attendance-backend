from sqlalchemy import Column, Integer, String, Date, Time, Float, DateTime
from database.db import Base
from datetime import datetime

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, index=True, nullable=False)
    date = Column(String, nullable=False)   # YYYY-MM-DD
    time = Column(String, nullable=False)   # HH:MM:SS
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    status = Column(String, default="Present")
    created_at = Column(DateTime, default=datetime.utcnow)
