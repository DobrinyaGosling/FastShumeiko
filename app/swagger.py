from fastapi import APIRouter
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html,
                                  get_swagger_ui_oauth2_redirect_html)

router = APIRouter()

SWAGGER_UI_OAUTH2_REDIRECT_URL = "/oauth2-redirect"

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",  # Укажите правильный путь к вашему OpenAPI JSON
        title="API - Swagger UI",
        oauth2_redirect_url=SWAGGER_UI_OAUTH2_REDIRECT_URL,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@router.get(SWAGGER_UI_OAUTH2_REDIRECT_URL, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@router.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",  # Укажите правильный путь к вашему OpenAPI JSON
        title="API - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )