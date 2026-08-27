from fastapi import Header, HTTPException

from database import supabase


def get_current_user(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Token Missing"
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    try:
        authenticated_user = supabase.auth.get_user(token).user
        return {
            "userId": str(authenticated_user.id),
            "email": authenticated_user.email,
            "name": (authenticated_user.user_metadata or {}).get("name"),
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")