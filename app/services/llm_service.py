from openai import AsyncOpenAI

from app.core.config import settings


class LLMServiceError(Exception):
    pass


async def generate_summary(text: str) -> str:

    # FREE MOCK MODE
    if settings.USE_MOCK_LLM:

        sentences = text.strip().split(".")

        summary = ". ".join(
            sentence.strip()
            for sentence in sentences[:2]
            if sentence.strip()
        )

        return summary + ("." if summary else "")

    # REAL OPENAI MODE
    client = AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        timeout=30.0,
        max_retries=0
    )

    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the text in 2 to 3 sentences using simple English."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        summary = response.choices[0].message.content

        if not summary or not summary.strip():
            raise LLMServiceError("Empty summary received")

        return summary.strip()

    except Exception as exc:
        print(f"OPENAI ERROR: {type(exc).__name__}: {exc}")
        raise LLMServiceError("Unable to generate summary") from exc

    finally:
        await client.close()