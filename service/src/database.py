import inspect
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Date, CheckConstraint,PickleType,DateTime,func,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import as_declarative

load_dotenv()
DB_URL = os.getenv("DB_HOST")
print(DB_URL)
engine = create_engine(DB_URL)
Base = declarative_base()

@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String)
    password = Column(String)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
class UploadLogs(Base):
    __tablename__ = "upload_logs"
    id = Column(Integer, primary_key=True,autoincrement=True)
    csv_url = Column(String)
    user_id = Column(String)
    uploaded_at = Column(Date)
    success = Column(Boolean, default=False)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True,autoincrement=True)
    appId = Column(Integer)
    name = Column(String)
    releaseDate = Column(Date)
    requiredAge = Column(Integer)
    price = Column(Integer)
    dlcCount = Column(Integer)
    aboutTheGame = Column(String)
    supportedLanguages = Column(String)
    windows = Column(Boolean)
    linux = Column(Boolean)
    mac = Column(Boolean)
    positive = Column(Integer)
    negative = Column(Integer)
    scoreRank = Column(Integer)
    developers = Column(String)
    publishers = Column(String)
    categories = Column(String)
    genres = Column(String)
    tags = Column(String)
    upload_log_id = Column(Integer)
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

def get_engine(): 
    return engine

Base.metadata.create_all(engine)