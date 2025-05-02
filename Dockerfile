
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pandas matplotlib requests lxml

ENTRYPOINT ["python", "exchanger.py"]