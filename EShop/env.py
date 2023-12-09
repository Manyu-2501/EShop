import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
PROJECT_SECRET_KEY = os.environ.get("PROJECT_SECRET_KEY")