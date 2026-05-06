# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

from workflows._wfr import wfr

# import routes
from routes.workflow import router as workflow_router
from routes.tasks import router as tasks_router

# (optional) shared HTTP client
import httpx


# ---- Lifespan (startup + shutdown) ----

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    wfr.start()

    app.state.http_client = httpx.AsyncClient()

    print("Workflow runtime started")

    yield


    await app.state.http_client.aclose()
    wfr.shutdown()

    print("Shutdown complete")


# ---- FastAPI app ----

app = FastAPI(
    title="Broker Workflow Service",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(workflow_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)