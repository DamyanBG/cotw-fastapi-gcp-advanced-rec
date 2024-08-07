from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers.routes import api_router
from async_job_scheduler import ascheduler
from es_queries.creator import create_es_indices, delete_es_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    ascheduler.start()
    print("Scheduler started")

    await create_es_indices()

    # await delete_es_index()

    yield

    ascheduler.shutdown()
    print("Scheduler shut down")


origins = ["*"]
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
