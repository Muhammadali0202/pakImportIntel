# ---- Base Image ----
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install Python dependencies first (for Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the frontend source code
COPY . .

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Start Streamlit on port 8080 bound to all interfaces
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
