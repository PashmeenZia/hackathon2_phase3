import os
from dotenv import load_dotenv

load_dotenv()

# Use NEON_DB_URL if available, otherwise fall back to DATABASE_URL
NEON_DB_URL = os.getenv("NEON_DB_URL")
DATABASE_URL = NEON_DB_URL or os.getenv("DATABASE_URL") or "sqlite:///./test.db"
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "dev-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))