import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    cognodb_uri: str = os.getenv("COGNODB_URI", "")
    cognodb_user: str = os.getenv("COGNODB_USER", "cognodb")
    cognodb_password: str = os.getenv("COGNODB_PASSWORD", "")
    flask_secret_key: str = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"

settings = Settings()
