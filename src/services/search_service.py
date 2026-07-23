"""Azure AI Search service for finance knowledge retrieval."""
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from src.config import settings


class SearchService:
    def __init__(self) -> None:
        self.client = SearchClient(
            endpoint=settings.azure_search_endpoint,
            index_name=settings.azure_search_index_finance,
            credential=AzureKeyCredential(settings.azure_search_api_key),
        )

    def search(self, query: str, top: int = 5) -> list[dict]:
        results = self.client.search(search_text=query, top=top)
        return [dict(result) for result in results]
