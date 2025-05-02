FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY exchanger.py .

VOLUME /app/data

ENV CSV_FILE=/app/data/rates.csv

ENTRYPOINT ["python", "exchanger.py"]

CMD ["--help"]