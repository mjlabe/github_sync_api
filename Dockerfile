FROM python:3.10-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -r requirements.txt

COPY src /src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8092"]
