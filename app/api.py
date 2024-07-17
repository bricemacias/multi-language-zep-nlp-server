from typing import Any, Dict

from fastapi import Depends, FastAPI, status
from starlette.responses import PlainTextResponse, RedirectResponse

from app.config import settings
from app.entity_extractor import SpacyExtractor, get_extractor
from app.entity_models import EntityRequest, EntityResponse

app = FastAPI(
    title="zep-nlp-server",
    version="0.3",
    description="Zep NLP Server",
)


@app.on_event("startup")
def startup_event() -> None:
    get_extractor()


@app.get("/healthz", response_model=str, status_code=status.HTTP_200_OK)
def health() -> PlainTextResponse:
    return PlainTextResponse(".")


@app.get("/config")
def config() -> Dict[str, Any]:
    """Get the current configuration."""
    return settings.dict()


@app.get("/", include_in_schema=False)
def docs_redirect() -> RedirectResponse:
    return RedirectResponse("/docs")


@app.post("/entities", response_model=EntityResponse)
def extract_entities(
    entity_request: EntityRequest,
    extractor: SpacyExtractor = Depends(get_extractor),
) -> EntityResponse:
    """Extract Named Entities from a batch of Records."""
    return extractor.extract_entities(entity_request.texts)
