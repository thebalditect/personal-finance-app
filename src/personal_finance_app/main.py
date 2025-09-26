from typing import Any
from fastapi import FastAPI

app = FastAPI()


@app.post("/")
def print_message() -> Any:
    return {"Hello": "World"}
