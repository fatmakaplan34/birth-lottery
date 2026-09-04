from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings
from app.routers.compare import router as compare_router
from app.routers.countries import router as countries_router
from app.routers.languages import router as languages_router
from app.routers.lottery import router as lottery_router
from app.routers.odds import router as odds_router


PRODUCTION = Settings.ENVIRONMENT == "production"
FRONTEND_DIST = Path(__file__).resolve().parents[1] / "frontend" / "dist"

app = FastAPI(
    title="The Birth Lottery",
    description="What are the odds of being born where you are?",
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=(
        r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
    ),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://www.googletagmanager.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https://flags.restcountries.com "
        "https://www.google-analytics.com https://*.google-analytics.com; "
        "connect-src 'self' https://www.google-analytics.com "
        "https://*.google-analytics.com https://www.googletagmanager.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'"
    )
    if PRODUCTION:
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    return response


if PRODUCTION:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        error: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={"detail": "Unexpected server error"},
        )


@app.get("/health", include_in_schema=False)
def health():
    return {
        "status": "alive",
        "project": "birth-lottery",
        "environment": Settings.ENVIRONMENT,
    }


app.include_router(countries_router)
app.include_router(languages_router)
app.include_router(compare_router)
app.include_router(lottery_router)
app.include_router(odds_router)

# Docker's frontend build is copied here. Keeping this mount last ensures API
# routes remain authoritative while production uses one public origin.
if FRONTEND_DIST.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIST, html=True),
        name="frontend",
    )
