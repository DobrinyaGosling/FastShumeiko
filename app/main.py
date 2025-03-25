from fastapi import FastAPI
from app.swagger import router as swagger_router
from app.hotels.routes import router as hotels_router
from app.users.routes import router as users_router
from app.bookings.routes import router as bookings_router
from app.auth.routes import router as auth_router

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/")
def get_index():
    return {"message": "It is FastAPI male)"}



app.include_router(swagger_router)
app.include_router(hotels_router)
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(auth_router)