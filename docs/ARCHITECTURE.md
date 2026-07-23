# Architecture

## Overview

Autonomous Finance Copilot is designed as a modular, service-oriented finance intelligence platform that combines API orchestration, multi-agent reasoning, retrieval, and medallion-based data processing.

## Architecture principle

The current platform prioritizes **clarity of orchestration over framework layering**. To reduce unnecessary complexity, agent management is centered on **Microsoft Foundry Agent Service first**. Additional tool abstraction frameworks such as **Semantic Kernel are intentionally deferred** until the runtime contracts, evaluation flows, and data platform integration patterns are mature.

## Logical architecture

```text
Client / BI / Workflow Caller
          |
          v
      FastAPI API
          |
          v
  Foundry Agent Orchestration
   |      |      |      |      |
   v      v      v      v      v
Variance Budget Forecast Vendor Anomaly
          \      |      /
           \     |     /
            Executive Summary
                  |
                  v
         Evaluation + API Response
```

## Platform components

### 1. API layer

`src/main.py` and `src/api/v1/*` expose REST endpoints for orchestration and specialist workflows.

Responsibilities:
- request validation
- routing
- middleware and tracing
- exception handling
- metrics exposure

### 2. Agent orchestration layer

`src/agents/` contains:
- shared contracts (`contracts.py`)
- base agent abstraction (`base.py`)
- agent instruction catalog (`instructions.py`)
- specialist finance agents
- orchestrator coordination logic

The orchestrator builds a shared `AgentContext`, dispatches specialist agents, and synthesizes results into an executive-level response.

### 3. Foundry integration layer

`src/services/foundry_client.py` and `src/services/foundry_agent_service.py` provide the Microsoft Foundry Agent Service integration boundary.

Responsibilities:
- create and access project clients
- define agent metadata and instructions
- execute agent runs
- provide the control plane seam for future production hardening

### 4. Retrieval layer

`src/services/search_service.py` wraps Azure AI Search.

Responsibilities:
- retrieve policy, finance, and knowledge artifacts
- support future RAG workflows
- expose search results to agents and orchestration pipelines

### 5. Data platform layer

`src/services/fabric_service.py` and `src/data/medallion/` align to a medallion architecture:

- **Bronze**: raw finance transaction ingestion
- **Silver**: validated and curated transformations
- **Gold**: KPI-ready aggregates and executive metrics

Delta table writes are currently implemented with `deltalake` write helpers.

### 6. Evaluation layer

`src/evaluation/scorer.py` provides a baseline evaluation mechanism for orchestrated runs.

Future evolution should include:
- factuality checks
- finance rule validation
- consistency scoring
- regression benchmarks
- human-in-the-loop review capture

## Data flow

1. Finance data lands in Bronze.
2. Bronze data is transformed into Silver curated datasets.
3. Gold datasets generate KPI summaries and metrics.
4. A caller invokes the FastAPI orchestration endpoint.
5. Foundry-managed orchestration coordinates specialist finance agents.
6. Specialist outputs are evaluated and consolidated.
7. Executive Summary Agent prepares a CFO-facing narrative.
8. FastAPI returns traceable structured results.

## Deployment architecture

Recommended production deployment targets:
- FastAPI container deployed to Azure Container Apps, AKS, or App Service
- Microsoft Foundry project hosting agent runtime resources
- Azure OpenAI model deployments
- Azure AI Search index for finance knowledge and embeddings
- Microsoft Fabric lakehouse / OneLake for persistent medallion storage
- GitHub Actions for CI/CD

## Future extensibility

Semantic Kernel may be introduced later as a complementary plugin and experimentation layer for:
- function and tool abstraction
- local experimentation
- reusable finance capability modules
- controlled prompt and tool iteration before production promotion

## Production hardening checklist

- Managed identity for service authentication
- Key Vault integration for secrets
- OpenTelemetry tracing and centralized logging
- API authentication and authorization
- stricter validation and schema versioning
- dataset lineage and observability
- robust retry, timeout, and circuit breaker policies
- infrastructure-as-code promotion across environments
