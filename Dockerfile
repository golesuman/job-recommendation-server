FROM python:3.9-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
# Allows docker to cache installed dependencies between builds
COPY requirements/requirements.txt /code/requirements.txt
COPY config/gunicorn/dev.py /code/gunicorn_config.py
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY src /code

EXPOSE 8000

RUN python manage.py migrate

CMD ["gunicorn", "--config", "gunicorn_config.py", "backend_api.wsgi:application"]