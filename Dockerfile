# Use an official Python image as the base
FROM python:3.9-slim

# Set a working directory inside the container
WORKDIR /workspace

# Install system dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy the requirements file to the container
COPY requirements.txt .

# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ensure that Python scripts in the container will be executable
CMD ["bash"]
