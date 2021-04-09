# Optional 2.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app_dogs

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app /app
