FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install django mysqlclient python-dotenv

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
