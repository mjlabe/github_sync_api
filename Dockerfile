FROM python:3.10-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install git

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -r requirements.txt

RUN mkdir /repos/
COPY src /src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8092"]
