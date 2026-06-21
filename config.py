import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "vertex_doc_secret")

    UPLOAD_FOLDER = "uploads"
    VECTOR_STORE = "vector_store"

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")