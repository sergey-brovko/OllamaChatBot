# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Создаем рабочую директорию
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./   /app/


# Set PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app

EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the bot when the container launches
CMD ["python", "main.py"]