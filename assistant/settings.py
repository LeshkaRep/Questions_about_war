from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные из .env
STATIC_URL = '/static/'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



