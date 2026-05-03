# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

from dapr.ext.workflow import WorkflowRuntime

# import your registration function
from app.dapr.workflow_runtime import register_workflows_and_activities

# import routes
from app.api.routes.workflow import router as workflow_router

# (optional) shared HTTP client
import httpx


# ---- Lifespan (startup + shutdown) ----

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    workflow_runtime = WorkflowRuntime()
    register_workflows_and_activities(workflow_runtime)
    workflow_runtime.start()

    app.state.http_client = httpx.AsyncClient()

    print("Workflow runtime started")

    yield


    await app.state.http_client.aclose()
    workflow_runtime.shutdown()

    print("Shutdown complete")


# ---- FastAPI app ----

app = FastAPI(
    title="Broker Workflow Service",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(workflow_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}