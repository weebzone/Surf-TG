FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install -U pip uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

CMD ["bash", "surf-tg.sh"]
