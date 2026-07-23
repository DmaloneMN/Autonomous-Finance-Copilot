"""Gold layer metric generation helpers."""
from __future__ import annotations

import pandas as pd
from deltalake import write_deltalake

from src.services.fabric_service import FabricService


class GoldLayerService:
    def __init__(self, fabric_service: FabricService) -> None:
        self.fabric_service = fabric_service

    def build_finance_kpis(self, dataframe: pd.DataFrame, dataset: str = "finance_kpis") -> str:
        summary = (
            dataframe.groupby("department", as_index=False)
            .agg(actual_amount=("actual_amount", "sum"), budget_amount=("budget_amount", "sum"))
        )
        summary["variance_pct"] = ((summary["actual_amount"] - summary["budget_amount"]) / summary["budget_amount"]) * 100
        relative_path = self.fabric_service.lakehouse_path("gold", dataset)
        write_deltalake(relative_path, summary, mode="overwrite")
        return relative_path
