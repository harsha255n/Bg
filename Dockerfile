
FROM python:3.10


WORKDIR /app


RUN apt-get update && apt-get install -y default-libmysqlclient-dev


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000


ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
