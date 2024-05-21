import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "Mail sender"
    DB_NAME = "amasender.db"
    PROJECT_DESCRIPTION = "email sender for Ama"

    BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

    admins = (
        os.getenv("ADMIN_ID"),
        os.getenv("ADMIN2_ID")
    )

    PROJECT_PATH = os.getenv("PROJECTPATH")
    DB_PATH = os.getenv("DBPATH")
    EMAIL = str(os.getenv("EMAIL"))
    EMAILPSWRD = str(os.getenv("PASSWORD"))


settings = Settings()
