from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False)  
    job_id = Column(String(255), unique=True, nullable=False) 
    status = Column(String(50), default="queued", nullable=False) 
