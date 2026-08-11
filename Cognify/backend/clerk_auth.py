import os
from fastapi import HTTPException, Request
from clerk_backend_api import Clerk
from dotenv import load_dotenv

load_dotenv()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

if not CLERK_SECRET_KEY:
    raise RuntimeError("CLERK_SECRET_KEY is missing from .env")


clerk = Clerk(bearer_token=CLERK_SECRET_KEY)


async def verify_clerk_token(request: Request):
    """
    Verify the Clerk session token sent by the frontend.
    """

    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header"
        )

    token = authorization.replace("Bearer ", "", 1)

    try:
        # Clerk SDK validates the session token
        session = clerk.sessions.verify_session(
            session_id=token
        )

        return session

    except Exception as e:
        print("Clerk verification error:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired Clerk token"
        )