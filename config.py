import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Get raw database URL
raw_db_url = os.getenv("DATABASE_URL")

def create_db_url(url: str) -> str:
    if not url or '://' not in url:
        raise ValueError("Invalid database URL")
    
    try:
        # Remove any quotes around the URL
        url = url.strip('"\'')
        
        # Split into protocol and rest
        protocol, rest = url.split('://', 1)
        
        # Split credentials and host
        credentials, host_part = rest.split('@', 1)
        
        # Split username and password
        if ':' in credentials:
            username, password = credentials.split(':', 1)
            # URL encode the password
            encoded_password = quote_plus(password)
            return f"{protocol}://{username}:{encoded_password}@{host_part}"
        
        return url
    except Exception as e:
        raise ValueError(f"Error parsing database URL: {str(e)}")

try:
    SUPABASE_DB_URL = create_db_url(raw_db_url)
    print("Database URL parsed successfully")  # Debug line
except ValueError as e:
    print(f"Error: {e}")
    raise