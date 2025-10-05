# Dockerfile

# Use a Python base image with necessary OS packages (MediaPipe often needs them)
# Updated, working line:
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /app

# Install system dependencies required by OpenCV and MediaPipe
# This is crucial for cloud deployment stability
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (main.py, movement_analyzer.py, etc.)
COPY . .

# Expose the port the FastAPI server will run on
EXPOSE 80

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]