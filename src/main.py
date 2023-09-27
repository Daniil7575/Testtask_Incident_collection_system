from fastapi import FastAPI

from src.incident.router import router as incident_touter


app = FastAPI(
    title="Incident Collection system",
    description="Test task incident collection system.",
    docs_url="/docs",
    redoc_url="/docs/redocs"
)

app.include_router(incident_touter)
