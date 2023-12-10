import json
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

__all__ = ['app']

app = FastAPI()

API_HOST = '0.0.0.0'
API_PORT = 5022


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


def start_api():
    import uvicorn
    print("Running the FastAPI application")
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)