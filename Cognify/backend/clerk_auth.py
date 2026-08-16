import os

from dotenv import load_dotenv
from fastapi import HTTPException, Request

from clerk_backend_api import (
    authenticate_request,
    AuthenticateRequestOptions,
)

load_dotenv()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_JWT_KEY = os.getenv("CLERK_JWT_KEY")

# Your Vite frontend URL
CLERK_AUTHORIZED_PARTY = os.getenv(
    "CLERK_AUTHORIZED_PARTY",
    "http://localhost:5173",
)

if not CLERK_SECRET_KEY:
    raise RuntimeError(
        "CLERK_SECRET_KEY is missing from .env"
    )


async def verify_clerk_token(request: Request):
    """
    Verify a Clerk session JWT sent by the React frontend.

    Frontend:
        Authorization: Bearer <Clerk session token>

    Returns:
        Clerk JWT payload containing `sub` (user ID).
    """

    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    try:
        state = authenticate_request(
            request,
            AuthenticateRequestOptions(
                secret_key=CLERK_SECRET_KEY,
                jwt_key=CLERK_JWT_KEY,
                authorized_parties=[
                    CLERK_AUTHORIZED_PARTY
                ],
                accepts_token=[
                    "session_token"
                ],
            ),
        )

        if not state.is_signed_in:
            reason = getattr(
                state,
                "reason",
                None,
            )

            raise HTTPException(
                status_code=401,
                detail=(
                    reason.name
                    if reason
                    else "Invalid or expired Clerk token"
                ),
            )

        if not state.payload:
            raise HTTPException(
                status_code=401,
                detail="Clerk token payload missing",
            )

        return state.payload

    except HTTPException:
        raise

    except Exception as e:
        print(
            "Clerk authentication error:",
            repr(e),
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired Clerk token",
        )
