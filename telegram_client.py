from pyrogram import Client
import os

app = Client(
    "user_session",  # Название сессии → создастся файл user_session.session
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)
