from fastapi import FastAPI
from app.routers.countries import router as countries_router
from app.routers.languages import router as languages_router
from app.routers.compare import router as compare_router
from app.routers.lottery import router as lottery_router
from app.routers.odds import router as odds_router
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI(
    title="The Birth Lottery",
    description="What are the odds of being born where you are?"
)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=(
        r"https?://(localhost|127\.0\.0\.1)(:\d+)?"
    ),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return{"status": "alive", "project": "birth-lottery"}

app.include_router(countries_router)
app.include_router(languages_router)
app.include_router(compare_router)
app.include_router(lottery_router)
app.include_router(odds_router)
