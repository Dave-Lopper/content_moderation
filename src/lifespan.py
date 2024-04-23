from contextlib import asynccontextmanager

rps_tracker = {}
models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    rps_tracker["request_count"] = 0
    rps_tracker["last_request_time"] = time.time()
    models["content_moderation"] = ContentModerator()
    yield
