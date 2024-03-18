FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache tesseract-ocr

# Install dependencies
COPY ../poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy the Django project code into the container
COPY ../../. /app/

# Expose the port on which Django runs
EXPOSE 8000

# download eng traindata for tesseract engine
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata -O /usr/share/tessdata/eng.traineddata

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
