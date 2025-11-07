from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import dataset, stats, calc

app = FastAPI(title="SolarTrace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Routers
app.include_router(dataset.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(calc.router, prefix="/api")