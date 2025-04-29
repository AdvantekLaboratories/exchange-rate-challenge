FROM python:3.13.1

ADD exchanger.py .
ADD rates.csv .

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "exchanger.py"]