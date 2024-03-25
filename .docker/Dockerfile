FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && apk add --no-cache tesseract-ocr

COPY ../poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY ../../. /app/

EXPOSE 8000

RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata -O /usr/share/tessdata/eng.traineddata

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
