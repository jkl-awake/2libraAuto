FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY 2libra_checkin.py /app/2libra_checkin.py

CMD ["python", "/app/2libra_checkin.py"]
