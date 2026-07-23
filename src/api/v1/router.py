"""Top-level API v1 router."""
from fastapi import APIRouter

from src.api.v1.endpoints import agents, analysis, anomaly, budget, forecast, reports, vendor

api_router = APIRouter()
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(budget.router, prefix="/budget", tags=["budget"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
api_router.include_router(vendor.router, prefix="/vendor", tags=["vendor"])
api_router.include_router(anomaly.router, prefix="/anomaly", tags=["anomaly"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
