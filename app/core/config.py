import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PORT = int(os.getenv("PORT"))
# SECRET_KEY = os.getenv("SECRET_KEY")