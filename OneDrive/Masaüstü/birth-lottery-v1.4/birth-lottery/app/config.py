import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RC_API_KEY = os.getenv("RC_API_KEY")
    COUNTRY_DATA_MODE = os.getenv(
        "COUNTRY_DATA_MODE",
        "live",
    ).strip().lower()
