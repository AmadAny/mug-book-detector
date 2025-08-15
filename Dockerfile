# Use an official Python runtime as a parent image
FROM python:3.9-slim

# --- Install system dependencies required by opencv-python-headless ---
# These are common libraries needed for OpenCV to function correctly,
# even in 'headless' mode within a container.
# libglib2.0-0: GLib library
# libsm6: X11 Session Management library
# libxext6: X11 extension library
# libxrender-dev: X11 Rendering Extension library
# libgomp1: GCC OpenMP library (often a dependency)
# libffi-dev: Foreign Function Interface library (sometimes needed)

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
