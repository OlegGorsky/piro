from pyrogram import Client
import os

app = Client(
    "user_session",  # Название .session файла
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)

app.start()  # Запросит ввод номера, кода и пароля
print("✅ Авторизация прошла успешно. Сессия сохранена.")
app.stop()
