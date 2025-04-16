
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.auth.routes import router2 as auth_lord_router
from app.auth.routes import router3 as utils_router
from app.bookings.routes import router as bookings_router
from app.hotels.routes import router as hotels_router
from app.hotels.routes import router2 as hotels_lord_router
from app.swagger import router as swagger_router
from app.users.routes import router as users_router

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/")
def get_index():
    return {"message": "It is FastAPI male)"}



app.include_router(swagger_router)
app.include_router(hotels_router)
app.include_router(hotels_lord_router)
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(auth_router)
app.include_router(auth_lord_router)
app.include_router(utils_router)


# Список разрешенных источников
origins = [
    "http://0.0.0.0:5500",  # React/Vue dev server
    "http://0.0.0.0:3000"  # React/Vue dev server
]

# Полная настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://0.0.0.0:5500"],  # Явно укажите фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)