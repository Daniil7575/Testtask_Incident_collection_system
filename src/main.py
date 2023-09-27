from fastapi import FastAPI


app = FastAPI(
    title="Incident Collection system",
    description="Test task incident collection system.",
    docs_url="/docs",
    redoc_url="/docs/redocs"
)