from database import engine
from sqlmodel import Session
from sqlalchemy import text

def test_connection():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection() 