from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///logs.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()

class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    log_type = Column(String(50))
    message = Column(Text)

Base.metadata.create_all(engine)
