"""Lazy embedding implementations used only for semantic project depth."""

from abc import ABC, abstractmethod
from functools import lru_cache
import httpx
from django.conf import settings


class BaseEmbeddingService(ABC):
    """Abstract sentence embedding interface."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Encode text strings as numeric vectors."""


class StubEmbeddingService(BaseEmbeddingService):
    """Deterministic local embedder for tests and explicit stub configuration."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [
            [
                float(sum(map(ord, token)) % 997) / 997
                for token in text.lower().split()[:16]
            ]
            or [0.0]
            for text in texts
        ]


class LocalEmbeddingService(BaseEmbeddingService):
    """Lazy-load a local sentence-transformers model on first invocation."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self._model = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(
                self.model_name, device="cpu", local_files_only=True
            )
        return self._model.encode(texts, normalize_embeddings=True).tolist()


class APIEmbeddingService(BaseEmbeddingService):
    """Call an OpenAI-compatible embeddings endpoint configured by the operator."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not settings.EMBEDDING_API_URL or not settings.EMBEDDING_API_KEY:
            raise RuntimeError("Embedding API URL and key must be configured.")
        response = httpx.post(
            settings.EMBEDDING_API_URL,
            json={"input": texts},
            headers={"Authorization": f"Bearer {settings.EMBEDDING_API_KEY}"},
            timeout=10,
        )
        response.raise_for_status()
        return [row["embedding"] for row in response.json()["data"]]


@lru_cache(maxsize=1)
def get_embedding_service() -> BaseEmbeddingService:
    """Return the process-cached embedding backend selected in settings."""
    backend = settings.EMBEDDING_BACKEND.lower()
    if backend == "stub":
        return StubEmbeddingService()
    if backend == "api":
        return APIEmbeddingService()
    if backend == "local":
        return LocalEmbeddingService(settings.EMBEDDING_MODEL)
    raise ValueError(f"Unsupported embedding backend: {backend}")
