"""Anomaly detection endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AnomalyRequest(BaseModel):
    fiscal_period: str
    sensitivity: float = 0.95


@router.post("/detect")
async def detect_anomalies(request: AnomalyRequest) -> dict[str, float | str]:
    return {
        "fiscal_period": request.fiscal_period,
        "sensitivity": request.sensitivity,
        "status": "queued",
    }
