# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY ./src /src

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

WORKDIR /src/rest

# Define the command to run the Flask app when the container starts
CMD ["python", "fd_api_flask.py"]
