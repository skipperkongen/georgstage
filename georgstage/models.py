from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)


class Shift(Base):
    __tablename__ = 'shift'
    year = Column(Unicode, primary_key=True)
    created_dt = Column(DateTime, nullable=False)
    ocean_dt = Column(DateTime, nullable=False)
    period_no = Column(Integer, nullable=False)  # 1-6
    shift_no = Column(Integer, nullable=False)  # 1-3


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    gast_no = Column(Integer, nullable=False) # 1-60
    period_no = Column(Integer, nullable=False)  # 1-6
    shift_no = Column(Integer, nullable=False) # 1-3
    task_code = Column(Unicode, nullable=False) # e.g. ve1




class Model:

    def __init__(self, dt):
        self.dt = dt


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

session.close()
