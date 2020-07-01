from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sailing(Base):
    __tablename__ = 'sailing'
    id = Column(Integer, primary_key=True)
    created_dt = Column(DateTime, nullable=False)
    tasks = relationship('Task')
    shifts = relationship('Shift')


class Shift(Base):
    __tablename__ = 'shift'
    id = Column(Unicode, primary_key=True)
    sailing_id = Column(Unicode, ForeignKey('sailing.id'))
    created_dt = Column(DateTime, nullable=False)
    ocean_dt = Column(DateTime, nullable=False)
    shift_no = Column(Integer, nullable=False)  # 1-6
    team_no = Column(Integer, nullable=False)  # 1-3


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    sailing_id = Column(Integer, ForeignKey('sailing.id'))
    created_dt = Column(DateTime, nullable=False)
    ocean_dt = Column(DateTime, nullable=False)
    gast_no = Column(Integer, nullable=False) # 1-60
    team_no = Column(Integer, nullable=False) # 1-3
    task_code = Column(Unicode, nullable=False) # e.g. ve1


engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

session.close()
