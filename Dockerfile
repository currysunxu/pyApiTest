FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN apt-get update -y
RUN apt-get install -y freetds-dev gcc

RUN pip install --no-cache-dir -r requirements.txt
COPY hostfile /tmp/
RUN cat /tmp/hostfile >>/etc/hosts

CMD ["python3"]