FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir --default-timeout=60 \
        -i https://pypi.tuna.tsinghua.edu.cn/simple \
        requests

COPY 2libra_checkin.py /app/2libra_checkin.py

CMD ["python", "/app/2libra_checkin.py"]
