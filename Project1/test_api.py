from fastapi import FastAPI

app = FastAPI(title="Test API")


@app.get("/")
async def root():
    return {"message": "Hello from test_api"}


@app.get("/ping", summary="Ping")
async def ping():
    return {"message": "pong"}


@app.get("/ping/{name}", summary="Ping with name")
async def ping_name(name: str):
    return {"message": f"pong, {name}"}


print(">>> Project1/test_api.py LOADED")