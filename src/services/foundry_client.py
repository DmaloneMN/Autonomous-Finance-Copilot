"""Factory for Microsoft Foundry project clients."""
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from src.config import settings


def build_project_client() -> AIProjectClient:
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    return AIProjectClient(endpoint=settings.foundry_project_endpoint, credential=credential)
