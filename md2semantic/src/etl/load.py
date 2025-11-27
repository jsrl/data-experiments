import structlog
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Session

from src.config import get_db_url

log = structlog.get_logger()

# 1. Define Model
class Base(DeclarativeBase):
    pass

class MarkdownFile(Base):
    __tablename__ = "markdown_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    content = Column(JSONB, nullable=False) # Structured sections
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 2. Load Logic
def load_to_postgres(data: list[dict]) -> None:
    """
    Load transformed markdown data into PostgreSQL database.

    Creates the markdown_files table if it doesn't exist and inserts
    all provided records in a single transaction.

    Args:
        data: List of dictionaries containing file_name, source_url, and sections

    Raises:
        Exception: If database connection fails or insertion fails
    """
    if not data:
        log.warning("No data to load.")
        return

    engine = create_engine(get_db_url())

    # Ensure table exists
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        try:
            objects = [
                MarkdownFile(
                    file_name=item["file_name"],
                    source_url=item["source_url"],
                    content=item["sections"]
                ) for item in data if item.get("sections")
            ]

            session.add_all(objects)
            session.commit()
            log.info("✅ Successfully loaded to Postgres", count=len(objects))
        except Exception as e:
            session.rollback()
            log.error("❌ Database insertion failed", error=str(e))
            raise
