from operator import imod


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"Hola": "mundo"}
