import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///finai.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True
