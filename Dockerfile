# Use an official Python runtime as a parent image
FROM python:3.9-slim

# --- Install system dependencies required by opencv-python-headless ---

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Note the updated comment about opencv-python-headless dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable (Optional, good practice)
ENV FLASK_APP=app.py

# Run the command to start the app when the container launches
CMD ["python", "app.py"]
