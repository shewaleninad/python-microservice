from fastapi import FastAPI

from app.routers import weather, joke, summary


app = FastAPI(
    title="Python Microservice",
    description="Weather, Joke and LLM Summary APIs",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "Python Microservice is running",
        "status": "success"
    }


app.include_router(weather.router)
app.include_router(joke.router)
app.include_router(summary.router)