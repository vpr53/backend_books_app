# Book Web (Django + Docker)

## Установка и запуск

1. Скопируйте `.env.example` в `.env` и измените настройки:

```bash
cp .env.example .env
```

2. Собрать и поднять контейнеры:

```bash
make up
```

- Django будет доступен на `http://localhost:8000`
- PostgreSQL внутри Docker с данными в volume `db-data`

3. Остановить контейнеры:

```bash
make stop 
```

---

## Makefile команды

```bash
# Запуск севера
make runserver

# Создать миграции
make makemigrations

# Применить миграции
make migrate

# Просмотр логов
make logs

# Остановить контейнеры
make stop
```

---

## Настройки файла .env

В `.env.example` есть настройки подключения к PostgreSQL:

```
DB_NAME=myadatabase
DB_USER=user
DB_PASSWORD=123123
DB_HOST=db
DB_PORT=5432
SECRET_KEY=ваш_секретный_ключ
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app_password
DEFAULT_FROM_EMAIL=example@gmail.com
```

---

## Примечания

- Все команды Django запускаются через Makefile — нет необходимости каждый раз писать длинные docker команды.
---

## Ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Poetry Documentation](https://python-poetry.org/)

