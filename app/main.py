from fastapi import FastAPI
from app.swagger import router as swagger_router
from app.routes.hotels import hotels_router
from app.routes.users import users_router

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/")
def get_index():
    return {"message": "It is FastAPI male)"}



app.include_router(swagger_router)
app.include_router(hotels_router)
app.include_router(users_router)