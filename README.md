# Autonomous Finance Copilot

Autonomous Finance Copilot is a **Foundry-first, FastAPI-based multi-agent finance platform** that integrates **Microsoft Fabric**, **Delta medallion pipelines**, **Azure OpenAI**, and **Azure AI Search**.

## Current architecture

This repository uses **Microsoft Foundry Agent Service as the primary multi-agent runtime and orchestration platform**. The current implementation focuses on:

- production-grade API structure with FastAPI
- finance agent coordination and orchestration
- Fabric-aligned data services
- Delta-based Bronze, Silver, and Gold medallion layers
- retrieval integration points with Azure AI Search
- evaluation scaffolding for agent outcomes
- Docker-based local development and deployment readiness

## What it does

The platform exposes a FastAPI API that coordinates specialized finance agents:

- Orchestrator Agent
- Variance Analysis Agent
- Budget Agent
- Forecast Agent
- Vendor Analysis Agent
- Anomaly Detection Agent
- Executive Summary Agent

These agents operate on finance data staged through Bronze, Silver, and Gold layers and are designed to support CFO, FP&A, procurement, and finance operations scenarios.

## Core capabilities

- FastAPI backend with versioned routes
- Microsoft Foundry Agent Service-oriented agent orchestration
- Azure OpenAI-backed model integration points
- Azure AI Search retrieval service scaffolding
- Microsoft Fabric / ADLS lakehouse integration scaffolding
- Medallion architecture services for Bronze, Silver, and Gold data zones
- Delta table write patterns via `deltalake`
- Evaluation scoring scaffold for agent outcomes
- Docker and docker-compose support

## Repository structure

```text
src/
  agents/             Foundry-managed finance agents and orchestration
  api/                FastAPI routes and endpoint contracts
  core/               middleware, logging, exceptions, DI
  data/medallion/     Bronze/Silver/Gold Delta pipeline services
  evaluation/         scoring and evaluation utilities
  services/           Foundry, Search, Fabric service integrations
infra/
  bicep/              Azure infrastructure templates
  github/             deployment reference assets
samples/
  datasets/           local CSV datasets for finance scenarios
tests/
  unit/               unit tests
  integration/        API/integration tests
.github/workflows/    CI/CD pipelines
docs/                 architecture and delivery docs
```

## Quick start

### 1. Clone and configure

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2. Run locally

```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

### 4. Run tests

```bash
pytest tests/ -v
```

## Environment variables

Configure the following in `.env`:

- Azure OpenAI endpoint and deployment settings
- Foundry project endpoint
- Azure AI Search endpoint and key
- Microsoft Fabric workspace and lakehouse identifiers
- ADLS connection string and container

See `.env.example` for the full list.

## API endpoints

- `GET /health`
- `POST /api/v1/agents/run`
- `POST /api/v1/analysis/variance`
- `POST /api/v1/budget/analyze`
- `POST /api/v1/forecast/generate`
- `POST /api/v1/vendor/analyze`
- `POST /api/v1/anomaly/detect`
- `POST /api/v1/reports/executive-summary`

## Future extensibility

**Semantic Kernel may be introduced later** as a complementary plugin and experimentation layer for tool/function abstraction, but it is intentionally **not a first-class dependency in the current implementation** while the core orchestration architecture is being stabilized.

## Delivery status

This repository currently provides a strong scaffold / MVP foundation. Some services, especially Foundry runtime execution and production deployment plumbing, are intentionally stubbed and should be hardened before enterprise rollout.

## Next recommended enhancements

- Implement full Foundry agent lifecycle operations
- Add real retrieval-augmented generation flows with Azure AI Search
- Persist Delta tables to configured lakehouse/object storage paths
- Add auth, RBAC, secrets management, telemetry, and policy enforcement
- Add richer evaluation benchmarks and regression testing
