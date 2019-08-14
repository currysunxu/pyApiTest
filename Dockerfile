FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN apt-get update -y
RUN apt-get install -y freetds-dev gcc

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python3"]