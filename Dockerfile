FROM python:3.12-slim-bookworm AS builder

COPY pyproject.toml poetry.lock ./

RUN apt update \
    && pip install poetry==1.8.3 \
    && apt install -y build-essential libmagic1 libmagic-dev \
    && poetry config virtualenvs.create false \
    && poetry install --only main \
    && rm -rf /var/lib/apt/lists/* /root/.cache

FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTEDECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -U app \
    && mkdir -p /app \
    && chown -R app:app /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=app:app . /app/

WORKDIR /app/src/

EXPOSE 8000

USER app
