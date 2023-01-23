# Базовый образ для сборки
FROM python:3.10-slim

# Указываем рабочую директорию
WORKDIR /app

# Запрещаем Python писать файлы .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает Python буферизировать stdout и stderr
ENV PYTHONBUFFERED 1

# Установка зависимостей проекта
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# Копируем проект
COPY . .

# Запускаем проект
#CMD ["uvicorn", "main:core", "--host", "0.0.0.0"]