# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy all necessary files into the container at /app
COPY requirements.txt prompts.py agents.py .env /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Load environment variables from .env file
ENV $(cat .env | xargs)

# Run agents.py when the container launches
CMD ["python", "agents.py"]
