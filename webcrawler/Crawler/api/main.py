from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.redisHelper import RedisClient
import json

__all__ = ['app']

app = FastAPI()

API_HOST = '0.0.0.0'
API_PORT = 5555

prefix = 'nimbus_nova'

def start_api():
    import uvicorn
    print("Running the FastAPI application")
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


@app.get('/zipcode/add/{zipcode}')
def add_zipcode(zipcode: str):
    conn = RedisClient(f"{prefix}", "zipcode")
    res = conn.set(zipcode, '1')
    msg = 'import successfully' if res else 'import failed'
    return json.dumps({'status': msg})


@app.get('/zipcode/get/all')
def get_zipcode():
    conn = RedisClient(f"{prefix}", "zipcode")
    return json.dumps({'status': list(conn.all().keys())})