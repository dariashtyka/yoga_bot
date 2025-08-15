# Use official Python 3.10 image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install system dependencies needed by OpenCV and MediaPipe
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1 \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies without cache to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Run your bot
CMD ["python", "bot.py"]