from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'msg':'This is a root endpoint'}

