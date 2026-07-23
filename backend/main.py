import logging
from contextlib import asynccontextmanager
from time import perf_counter

from api.routers.category import router as category_router
from api.routers.task import router as task_router
from core.config import get_settings
from core.logging import configure_logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
configure_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Base.metadata.create_all(bind=engine)
    app.state.request_count = 0
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=category_router)


logger = logging.getLogger("app.middleware")


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.middleware("http")
async def request_number_header(request: Request, call_next) -> Response:
    request.app.state.request_count += 1
    request_count = request.app.state.request_count
    try:
        response: Response = await call_next(request)
    except:
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path,
        )
        raise

    response.headers["X-Request-Number"] = str(request_count)
    return response


app.add_middleware(
    CORSMiddleware, allow_origins=settings.allow_origins, allow_methods=["*"]
)
