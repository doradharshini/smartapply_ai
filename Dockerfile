FROM python:3.11-slim

WORKDIR /app

# Copy requirement and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into docker
COPY . .

# Expose port for ADK web server (Cloud Run)
EXPOSE 8080

# Set environment variables for Cloud Run
ENV HOST=0.0.0.0
ENV PORT=8080

# Ensure standard output doesn't buffer and break MCP stdio
ENV PYTHONUNBUFFERED=1

# Start the ADK web server
CMD ["adk", "web", "--port", "8080", "--host", "0.0.0.0"]
