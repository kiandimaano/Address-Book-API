import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

logger = logging.getLogger(__name__)

# Initialize db engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} 
)

# Session factory for generating isolated database connections
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy data models"""
    pass

def get_db():
    """
    Create database session per request then cleanup
    """
    db = session_local()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()