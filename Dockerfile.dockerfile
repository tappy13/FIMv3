# First stage: build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Second stage: minimal image with the dependencies
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app /app

# Expose Flask port
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
