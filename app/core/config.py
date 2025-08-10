from dotenv import load_dotenv
import os
from pathlib import Path

# Get absolute path to .env file in project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"Loading .env from: {ENV_PATH}")  # debug

load_dotenv(dotenv_path=ENV_PATH)

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

print("Loaded DB Name:", MONGO_DB_NAME)  # debug
