from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:6vFvzWwpso6K0oCKxpdD@jalen-data.czawitrflbjp.us-east-1.rds.amazonaws.com/postgres"

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
