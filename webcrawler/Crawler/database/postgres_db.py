from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# print("Loading PostgreSQL Environment Variables...")
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
# print("PostgreSQL Environment Variables Loaded: %s", SQLALCHEMY_DATABASE_URL)
logging.info("Connecting to PostgreSQL...")
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=100)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
logging.info("Connection to PostgreSQL Successful!")
