from starlette.requests import Request
from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO

from queries.user_queries import insert_user, select_user_by_email
from models.user_models import UserCreate
from auth.token import create_access_token
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    "http://localhost:8000/google-auth/callback",
    allow_insecure_http=True,
)

google_auth_router = APIRouter(prefix="/google-auth")


@google_auth_router.get("/login", tags=["Google SSO"])
async def google_login():
    return await google_sso.get_login_url(
        redirect_uri="http://localhost:8000/google-auth/callback",
        params={"prompt": "consent", "access_type": "offline"},
    )


@google_auth_router.get("/callback", tags=["Google SSO"])
async def google_callback(request: Request):
    user = await google_sso.verify_and_process(request)
    user_stored = await select_user_by_email(user.email)
    if not user_stored:
        user_to_add = UserCreate(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        user_stored = await insert_user(user_to_add)
    token = create_access_token(user_stored)
    response = RedirectResponse(
        url=f"http://localhost:3000/google-auth?token={token}",
        status_code=status.HTTP_302_FOUND,
    )
    return response
