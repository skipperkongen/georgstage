from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Trip(Base):
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False, unique=True)
    tasks = relationship('Task')


class Watch(Base):
    __tablename__ = 'watch'
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trip.id'))
    date = Column(DateTime, nullable=False)
    watch_no = Column(Integer, nullable=False)  # 1-6
    team_no = Column(Integer, nullable=False)  # 1-3


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trip.id'))
    date = Column(DateTime, nullable=False)
    sailor_no = Column(Integer, nullable=False) # 1-60
    task_code = Column(Integer, nullable=False)


engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

session.close()
