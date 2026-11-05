from fastapi import APIRouter, HTTPException

from app.services.joke_service import (
    fetch_joke,
    JokeUpstreamError
)

from app.schemas.response import JokeResponse


router = APIRouter(
    tags=["Joke"]
)


@router.get(
    "/joke",
    response_model=JokeResponse
)
async def get_joke():

    try:
        result = await fetch_joke()
        return result

    except JokeUpstreamError:
        raise HTTPException(
            status_code=502,
            detail="Joke provider is unavailable"
        )