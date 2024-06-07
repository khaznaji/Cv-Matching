# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /python-docker

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
