# Use Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Create the logs directory to avoid FileNotFoundError
RUN mkdir -p /app/logs

# Copy all project files into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./utils/wait-for-it.sh /usr/local/bin/wait-for-it.sh

RUN chmod +x /usr/local/bin/wait-for-it.sh

# Define the command to run Faust
ENTRYPOINT ["wait-for-it.sh", "kafka-00:9092", "--", "faust", "-A", "app.main", "worker", "-l", "info"]
