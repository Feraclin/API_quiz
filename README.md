## Структура
```
project
├── api1
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── alembic
│   │   ├── versions
│   │   │   └── __init__.py
│   │   └── alembic.ini
│   ├── Dockerfile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── requirements.txt
├── db
│   ├── Dockerfile
│   └── init.sql
└── docker-compose.yml
```

## описание каталогов и файлов:

- `api1/`  Каталог для API.
  - `app/`: Каталог приложения FastAPI.
  - `alembic/`: Каталог для Alembic, используемого для миграций базы данных.
  - `poetry.lock`: Файл, сгенерированный Poetry, содержащий фиксированные версии зависимостей проекта.
  - `pyproject.toml`: Файл проекта Poetry, содержащий список зависимостей и другую конфигурацию проекта.
  - `requirements.txt`: Файл зависимостей Python для обратной совместимости.

- `db/`: Каталог для контейнера базы данных PostgreSQL.
  - `Dockerfile`: Файл Dockerfile для контейнера базы данных.
  - `init.sql`: Файл инициализации базы данных, содержащий SQL-скрипты для создания таблиц и других необходимых объектов.

- `docker-compose.yml`: Файл конфигурации Docker Compose для создания и настройки контейнеров.


Кроме того, файлы `poetry.lock` и `pyproject.toml` добавлены для управления зависимостями с помощью Poetry.