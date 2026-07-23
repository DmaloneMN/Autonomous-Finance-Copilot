"""Variance analysis endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class VarianceRequest(BaseModel):
    fiscal_period: str
    department: str | None = None


@router.post("/variance")
async def variance_analysis(request: VarianceRequest) -> dict[str, str | None]:
    return {
        "fiscal_period": request.fiscal_period,
        "department": request.department,
        "status": "queued",
    }
