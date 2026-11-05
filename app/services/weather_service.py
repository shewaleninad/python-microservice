import httpx


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


class CityNotFoundError(Exception):
    pass


class WeatherUpstreamError(Exception):
    pass


def get_weather_condition(code: int) -> str:
    conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return conditions.get(code, "Unknown weather condition")


async def fetch_weather(city: str) -> dict:
    city = city.strip()

    if not city:
        raise CityNotFoundError("City name cannot be empty")

    timeout = httpx.Timeout(10.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:

            # 1. Find city coordinates
            geo_response = await client.get(
                GEOCODING_URL,
                params={
                    "name": city,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
            )

            geo_response.raise_for_status()
            geo_data = geo_response.json()

            results = geo_data.get("results")

            if not results:
                raise CityNotFoundError(
                    f"City '{city}' not found"
                )

            location = results[0]

            latitude = location["latitude"]
            longitude = location["longitude"]
            city_name = location["name"]

            # 2. Fetch current weather
            weather_response = await client.get(
                WEATHER_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "weather_code"
                    ),
                    "timezone": "auto",
                },
            )

            weather_response.raise_for_status()
            weather_data = weather_response.json()

            current = weather_data.get("current")

            if not isinstance(current, dict):
                raise WeatherUpstreamError(
                    "Invalid weather response"
                )

            temperature = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            weather_code = current.get("weather_code")

            if (
                temperature is None
                or humidity is None
                or weather_code is None
            ):
                raise WeatherUpstreamError(
                    "Incomplete weather information"
                )

            return {
                "city": city_name,
                "temperature": temperature,
                "condition": get_weather_condition(
                    int(weather_code)
                ),
                "humidity": humidity,
            }

    except (CityNotFoundError, WeatherUpstreamError):
        raise

    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise WeatherUpstreamError(
            "Weather provider is currently unavailable"
        ) from exc