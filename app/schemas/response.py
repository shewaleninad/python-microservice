from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: int


class JokeResponse(BaseModel):
    joke: str
    category: str


class SummaryRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str