FROM python:3.11-slim

WORKDIR /project

# Copy requirement and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into docker
COPY . .

# Ensure standard output doesn't buffer and break MCP stdio
ENV PYTHONUNBUFFERED=1

# Run the agent directly for demonstration purposes
CMD ["python", "app/ai_agent/eligibility_agent.py"]
