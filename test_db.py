import psycopg2
from config import SUPABASE_DB_URL

def test_direct_connection():
    try:
        conn = psycopg2.connect(SUPABASE_DB_URL)
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {str(e)}")

if __name__ == "__main__":
    test_direct_connection() 