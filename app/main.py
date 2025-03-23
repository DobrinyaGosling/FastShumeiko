from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_index():
    return {"message": "It is FastAPI male)"}