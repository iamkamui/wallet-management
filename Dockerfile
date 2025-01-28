FROM python:latest

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/backend
COPY requirements.txt ${WORKDIR}
RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt