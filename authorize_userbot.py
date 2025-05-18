from pyrogram import Client
import os

app = Client(
    "user_session",  # Создаст user_session.session
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)

app.start()
print("✅ Авторизация завершена. Сессия сохранена.")
app.stop()
