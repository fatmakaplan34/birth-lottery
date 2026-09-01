from fastapi import APIRouter, HTTPException

from app.services.languages import get_language_data


router = APIRouter(
    prefix="/languages",
    tags=["languages"],
)


@router.get("/{language_name}")
async def get_language(language_name: str):
    try:
        return await get_language_data(language_name)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error