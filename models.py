from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key = True, index = True)
    name = Column (String, index = True)
    description = Column(String, nullable= True)
    created_at = Column(DateTime, default= datetime.now)
    is_completed_today = Column(Boolean, default = False)

    