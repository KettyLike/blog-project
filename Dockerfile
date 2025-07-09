# Базовий образ з Python
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Відкриваємо порт 8000
EXPOSE 8000

# Запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
