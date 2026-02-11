# ------------------ Build Stage ------------------
    FROM python:3.11-slim AS builder

    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # Install build tools
    RUN apt-get update && apt-get install -y build-essential
    
    # Copy dependency list first for caching
    COPY requirements.txt .
    
    # Install dependencies to an isolated prefix
    RUN pip install --upgrade pip && \
        pip install --prefix=/install -r requirements.txt
    
    # ------------------ Final Stage ------------------
    FROM python:3.11-slim
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # Copy installed dependencies
    COPY --from=builder /install /usr/local
    
    # Copy backend application code
    COPY ./app ./app
    
    # Expose the app port
    EXPOSE 8000
    
    # Default command to run FastAPI via Uvicorn
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    