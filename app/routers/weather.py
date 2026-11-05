from fastapi import APIRouter, HTTPException, Query

from app.services.weather_service import (
    fetch_weather,
    CityNotFoundError,
    WeatherUpstreamError,
)

from app.schemas.response import WeatherResponse


router = APIRouter(
    tags=["Weather"]
)


@router.get(
    "/weather",
    response_model=WeatherResponse
)
async def get_weather(
    city: str = Query(
        ...,
        min_length=1,
        description="Enter city name"
    )
):
    try:
        result = await fetch_weather(city)
        return result

    except CityNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )

    except WeatherUpstreamError:
        raise HTTPException(
            status_code=502,
            detail="Weather provider is unavailable"
        )