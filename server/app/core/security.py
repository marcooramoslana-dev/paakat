from fastapi import Header, HTTPException, status

from app.core.config import get_settings


async def verify_api_key(x_api_key: str = Header(default="")) -> None:
    """Valida la API key solo si API_KEY esta configurada (no vacia)."""
    settings = get_settings()
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key invalida o ausente",
        )
