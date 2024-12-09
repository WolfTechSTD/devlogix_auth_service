FROM python:3.12.3 AS build

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

FROM build AS app

ADD . /app

WORKDIR /app

RUN uv sync --frozen --no-dev

RUN uv pip install "gunicorn<=23.0.0"

CMD uv run gunicorn "app.main:get_app()" --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
