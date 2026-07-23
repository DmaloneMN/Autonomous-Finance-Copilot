"""Vendor analysis endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class VendorRequest(BaseModel):
    vendor_id: str | None = None
    fiscal_period: str


@router.post("/analyze")
async def vendor_analysis(request: VendorRequest) -> dict[str, str | None]:
    return {
        "fiscal_period": request.fiscal_period,
        "vendor_id": request.vendor_id,
        "status": "queued",
    }
