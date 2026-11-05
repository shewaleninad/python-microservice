import httpx


JOKE_API_URL = (
    "https://official-joke-api.appspot.com/random_joke"
)


class JokeUpstreamError(Exception):
    pass


async def fetch_joke() -> dict:

    timeout = httpx.Timeout(10.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:

            response = await client.get(JOKE_API_URL)

            response.raise_for_status()

            data = response.json()

            setup = data.get("setup")
            punchline = data.get("punchline")
            category = data.get("type")

            if not all(
                isinstance(value, str) and value.strip()
                for value in (setup, punchline, category)
            ):
                raise JokeUpstreamError(
                    "Invalid joke API response"
                )

            return {
                "joke": f"{setup} {punchline}",
                "category": category
            }

    except JokeUpstreamError:
        raise

    except (httpx.HTTPError, ValueError, TypeError) as exc:
        raise JokeUpstreamError(
            "Joke provider is currently unavailable"
        ) from exc