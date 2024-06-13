from backend.db import SessionLocal


async def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()