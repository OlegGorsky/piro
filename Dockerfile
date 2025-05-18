FROM python:3.11-slim

WORKDIR /app

# Явно копируем сессию (важно, если она не в .dockerignore)
COPY user_session.session ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
