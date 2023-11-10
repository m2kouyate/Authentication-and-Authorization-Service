FROM python:3.9-slim

# Установка рабочую директорию в контейнере
WORKDIR /app

# Копирование файлов зависимостей в рабочую директорию
COPY requirements.txt /app/

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование оставшуейся части кода проекта в рабочую директорию
COPY . /app/

# Порт, который будет открыт контейнером
EXPOSE 8000

# Переменные окружения (при необходимости)
# ENV VARIABLE_NAME=value

# Команда для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "auth.wsgi:application"]
