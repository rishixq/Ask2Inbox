import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# ---------------------------
# Load .env Config
# ---------------------------
load_dotenv()

DATABASE_URL = os.getenv("SUPABASE_DB_URL")

if not DATABASE_URL:
    raise ValueError("❌ SUPABASE_DB_URL not found in .env file")


# ---------------------------
# Create SQLAlchemy Engine
# ---------------------------
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)


# ---------------------------
# Session Local (Thread Safe)
# ---------------------------
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


# ---------------------------
# Base ORM Class
# ---------------------------
Base = declarative_base()


# ---------------------------
# Dependency to Get DB Session
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Test Database Connection
# ---------------------------
def test_connection():
    """Verifies whether the connection to Supabase PostgreSQL works."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful:", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", e)
        raise e


if __name__ == "__main__":
    test_connection()
