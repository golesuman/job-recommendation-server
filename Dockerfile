# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE=backend_api.settings
# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port your Django application will run on (usually 8000)
EXPOSE 8000

# Start the application using Gunicorn or another WSGI server
CMD ["python", "/app/src/manage.py", "runserver", "0.0.0.0:8000"]  
