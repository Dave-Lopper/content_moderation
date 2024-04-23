import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from loguru import logger

from src.routes import moderation_router

rps_tracker = {}
logger.add("api.log")


def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        rps_tracker["request_count"] = 0
        rps_tracker["last_request_time"] = time.time()
        yield

    app = FastAPI(title="Content moderation API", lifespan=lifespan)
    app.include_router(moderation_router)

    @app.middleware("http")
    async def log_rps(request: Request, call_next):
        rps_tracker["request_count"] += 1

        current_time = time.time()
        if current_time - rps_tracker["last_request_time"] >= 1:
            rps = rps_tracker["request_count"] / (
                current_time - rps_tracker["last_request_time"]
            )
            logger.info(f"[Requests per second]: {rps:.2f}")
            rps_tracker["request_count"] = 0
            rps_tracker["last_request_time"] = current_time

        response = await call_next(request)
        return response

    return app
