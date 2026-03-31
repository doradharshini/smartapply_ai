# SmartApply AI

SmartApply AI is a comprehensive AI-powered application that seamlessly analyzes user profiles against various government schemes and public assistance programs to determine eligibility and recommend the best options.

Built for seamless performance, it leverages an uncoupled architecture linking the **Google Agent Development Kit (ADK)** with standard datasets via **Model Context Protocol (MCP)**. Everything runs locally inside Docker, but it is fundamentally designed for robust cloud deployment on **Google Cloud Run**.

---

## Architecture

```mermaid
flowchart LR
  Citizen["👤 Citizen Request"]
  UI["💬 Chat/Web UI"]
  CloudRun["☁️ Cloud Run Service"]
  Guardrails["🛡️ Validation + Guardrails"]
  Agent["🤖 ADK Agent"]
  MCP["⚙️ FastMCP Server"]
  DB["📊 JSON Database"]
  Guidance["✅ Guidance"]

  Vertex["🧠 Vertex AI<br/>(Gemini 2.5 Flash)"]
  ADC["🔐 ADC Auth (No API Keys)"]
  Logs["📈 Logs + Metrics"]

  Citizen -->|"1. Profile"| UI -->|"request"| CloudRun -->|"validate"| Guardrails --> Agent
  Agent -->|"2. Tool Call"| MCP
  MCP -->|"3. Query"| DB
  DB -.->|"4. Data"| MCP
  MCP -.->|"5. Response"| Agent
  Agent ==>|"6. Advice"| Guidance

  Agent -.->|"model call"| Vertex
  ADC -.->|"auth"| Vertex
  Vertex -.->|"completion"| Agent

  CloudRun -.-> Logs
  Agent -.-> Logs
  MCP -.-> Logs

  style Citizen fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style UI fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style CloudRun fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style Guardrails fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style Agent fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style Vertex fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style ADC fill:#E8F0FE,stroke:#4285F4,color:#4285F4,stroke-width:2px
  style MCP fill:#FEF7E0,stroke:#FBBC05,color:#E37400,stroke-width:2px
  style DB fill:#E6F4EA,stroke:#34A853,color:#137333,stroke-width:2px
  style Guidance fill:#FCE8E6,stroke:#EA4335,color:#C5221F,stroke-width:2px
  style Logs fill:#ffffff,stroke:#bdc1c6,color:#5f6368,stroke-width:2px
```

1. **MCP Server (`mcp_main.py`)**: Built with FastMCP to expose a structured scheme catalog (`database.json`) over MCP tools.
2. **ADK Agent (`smartapply_agent/agent.py`)**: A Google ADK `LlmAgent` running `gemini-2.5-flash` (Vertex AI) and calling MCP tools over stdio.

---

## Quickstart (Local)

1. Make sure Python 3.11 is installed.
2. Install dependencies:
   ```bash
   cd smartapply_ai
   pip install -r requirements.txt
   ```
3. Authenticate with Google Cloud (ADC):
   ```bash
   gcloud auth application-default login
   ```
4. Set Vertex AI env vars (copy `.env.example` to `.env` or export env vars):
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```
5. Run ADK Dev UI:
   ```bash
   adk web
   ```

---

## Google Cloud Run Deployment

### Build + Deploy (same pattern as NextMove)

```bash
gcloud services enable aiplatform.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/smartapply-ai
gcloud run deploy smartapply-ai \
  --image gcr.io/YOUR_PROJECT_ID/smartapply-ai \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1" \
  --memory=1Gi \
  --timeout=300
```

### Get the Cloud Run URL (one-liner)

```bash
gcloud run services describe smartapply-ai --region us-central1 --format="value(status.url)"
```
