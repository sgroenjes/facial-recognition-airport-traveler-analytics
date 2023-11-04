# db_init.py
# Database initialization and schema definition.
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

# Load environment variables
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# Define the PostgreSQL URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Check if the database does not exist, if it doesn't, create it
if not database_exists(engine.url):
  create_database(engine.url)

# Define a base class
Base = declarative_base()

# Define the User model
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  username = Column(String, unique=True, nullable=False)
  email = Column(String, unique=True, nullable=False)
  created_at = Column(DateTime, nullable=False)

  # Define the relationship to AccessLog
  access_logs = relationship('AccessLog', back_populates='user')

# Define the AccessLog model
class AccessLog(Base):
  __tablename__ = 'access_logs'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  accessed_at = Column(DateTime, nullable=False)
  event = Column(String, nullable=False)

  # Define the relationship to User
  user = relationship('User', back_populates='access_logs')

# Create all tables in the engine
Base.metadata.create_all(engine)
