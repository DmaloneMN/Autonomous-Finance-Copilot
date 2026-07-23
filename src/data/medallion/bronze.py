"""Bronze layer ingestion models and Delta write helpers."""
from __future__ import annotations

import pandas as pd
from deltalake import write_deltalake

from src.services.fabric_service import FabricService


class BronzeLayerService:
    def __init__(self, fabric_service: FabricService) -> None:
        self.fabric_service = fabric_service

    def write_transactions(self, dataframe: pd.DataFrame, dataset: str = "finance_transactions") -> str:
        relative_path = self.fabric_service.lakehouse_path("bronze", dataset)
        write_deltalake(relative_path, dataframe, mode="overwrite")
        return relative_path
