"""Drop idea_status enum if it exists."""
from sqlalchemy import create_engine, text
from src.config.settings import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text('DROP TYPE IF EXISTS idea_status CASCADE'))
    conn.commit()
    print('✅ Dropped idea_status enum')
