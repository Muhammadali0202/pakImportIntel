# ---- Lightweight Base Image ----
FROM python:3.11-slim

# Minimal system deps — only what PyMuPDF needs for PDF text extraction
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install lightweight Python dependencies
COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Copy the backend source code
COPY . .

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
