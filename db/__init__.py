from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = ""

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=5
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
