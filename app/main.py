from fastapi import FastAPI
from app.database import engine
from app.models import user, ride_pool, ride_request, ride_pool_member

app = FastAPI()

user.Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.api.ride_routes import router as ride_router

app = FastAPI()

app.include_router(ride_router)


from fastapi import FastAPI
from app.api.ride_routes import router as ride_router
from app.core.logging_config import setup_logging
import logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(ride_router)

logger.info("Smart Airport Ride Pooling Backend Started")


from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"Completed {request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Time: {round(process_time, 4)}s"
    )

    return response
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
