FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY shared/permissions.py ./shared/permissions.py

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "ai_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
