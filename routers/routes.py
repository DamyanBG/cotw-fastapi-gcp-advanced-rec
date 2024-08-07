from fastapi import APIRouter

from routers import (
    user_route,
    image_route,
    cat_route,
    votes_route,
    dummy_data_route,
    google_auth_route,
)


api_router = APIRouter()
api_router.include_router(user_route.user_router)
api_router.include_router(image_route.images_router)
api_router.include_router(cat_route.cats_router)
api_router.include_router(votes_route.votes_router)
api_router.include_router(dummy_data_route.dummy_data_router)
api_router.include_router(google_auth_route.google_auth_router)
