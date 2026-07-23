"""Forecast endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ForecastRequest(BaseModel):
    fiscal_period: str
    horizon_months: int = 3


@router.post("/generate")
async def generate_forecast(request: ForecastRequest) -> dict[str, int | str]:
    return {
        "fiscal_period": request.fiscal_period,
        "horizon_months": request.horizon_months,
        "status": "queued",
    }
