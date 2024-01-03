FROM python:3.10.13-alpine

WORKDIR /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

CMD [ "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
