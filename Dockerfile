# Используем Python 3.12 slim
FROM python:3.12-slim

# Отключаем создание pyc и включаем буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Устанавливаем системные зависимости для сборки и psycopg
RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl build-essential && \
    apt-get clean

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем pyproject.toml и poetry.lock и ставим зависимости
COPY pyproject.toml poetry.lock ./ 
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем весь проект
COPY . .

# Команда по умолчанию для dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
