from fastapi import FastAPI

app = FastAPI()


@app.post("/")
def print_message():
    return {"Hello": "World"}
