import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL = "claude-opus-4-6"
    MAX_FILE_SIZE_MB = 20
    UPLOAD_FOLDER = "/tmp/cfo_uploads"
