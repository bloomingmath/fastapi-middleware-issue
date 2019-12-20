import time
from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.testclient import TestClient
import pytest

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("page.html", {"request": request})

client = TestClient(app)

@pytest.mark.asyncio
async def test_middleware():
    from async_asgi_testclient import TestClient

    async with TestClient(app) as client:
        response = await client.get("/")
        assert "X-Process-Time" in response.headers