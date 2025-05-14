FROM python:latest
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/backend

COPY . /usr/src

ENV PATH="/usr/src/.venv/bin:$PATH"

RUN uv sync --locked
