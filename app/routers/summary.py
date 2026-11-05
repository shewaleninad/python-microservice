from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.core.config import settings
from app.core.security import verify_api_key

from app.services.llm_service import (
    generate_summary,
    LLMServiceError
)

from app.schemas.response import (
    SummaryRequest,
    SummaryResponse
)


router = APIRouter(
    tags=["Summary"]
)


@router.post(
    "/summary",
    response_model=SummaryResponse
)
async def create_summary(
    request: SummaryRequest,
    authenticated: bool = Depends(verify_api_key)
):

    # Validate empty text
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty"
        )

    # Validate maximum text length
    if len(request.text) > settings.MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Text exceeds maximum allowed length "
                f"of {settings.MAX_TEXT_LENGTH} characters"
            )
        )

    try:
        summary = await generate_summary(request.text)

        return {
            "summary": summary
        }

    except LLMServiceError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="LLM provider is currently unavailable"
        )