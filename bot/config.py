import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('MAX_BOT_TOKEN', '')
MAX_BASE_URL: str = os.getenv('MAX_BASE_URL', 'https://platform-api2.max.ru')
WEBAPP_URL: str = os.getenv('WEBAPP_URL', 'http://localhost:3000')
BACKEND_URL: str = os.getenv('BACKEND_URL', 'http://localhost:8000')
