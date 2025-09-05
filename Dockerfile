FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD [ "uv", "run", "main.py" ]
