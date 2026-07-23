"""Microsoft Fabric and ADLS integration service."""
from __future__ import annotations

from azure.storage.filedatalake import DataLakeServiceClient

from src.config import settings


class FabricService:
    def __init__(self) -> None:
        self.workspace_id = settings.fabric_workspace_id
        self.lakehouse_id = settings.fabric_lakehouse_id
        self.client = DataLakeServiceClient.from_connection_string(settings.adls_connection_string)

    def lakehouse_path(self, zone: str, dataset: str) -> str:
        return f"{zone}/{dataset}"

    def list_paths(self, zone: str) -> list[str]:
        file_system_client = self.client.get_file_system_client(settings.adls_container)
        paths = file_system_client.get_paths(path=zone)
        return [path.name for path in paths]
