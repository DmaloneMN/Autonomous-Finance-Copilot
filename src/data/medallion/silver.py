"""Silver layer transformation helpers."""
from __future__ import annotations

import pandas as pd
from deltalake import write_deltalake

from src.services.fabric_service import FabricService


class SilverLayerService:
    def __init__(self, fabric_service: FabricService) -> None:
        self.fabric_service = fabric_service

    def build_curated_spend(self, dataframe: pd.DataFrame, dataset: str = "curated_spend") -> str:
        transformed = dataframe.copy()
        transformed["variance"] = transformed["actual_amount"] - transformed["budget_amount"]
        relative_path = self.fabric_service.lakehouse_path("silver", dataset)
        write_deltalake(relative_path, transformed, mode="overwrite")
        return relative_path
