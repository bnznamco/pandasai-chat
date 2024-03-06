FROM python:3.11


ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/api

WORKDIR /app

COPY ./requirements.txt /app/api/

RUN pip install -r ./api/requirements.txt

CMD ["uvicorn", "api.app:app", "--reload", "--host", "0.0.0.0"]
