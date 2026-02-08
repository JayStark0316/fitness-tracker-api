from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import JSONResponse

from commons.utils.database import db_manager
from commons.exceptions.base_api_exception_handler import BaseAPIException
from commons.exceptions.default_error_api_response import DefaultApiErrorResponse

from users.user_router import router as user_router

from commons.utils.logger_config import api_logger


# ------------------------------
# Life Span Handler
# ------------------------------
@asynccontextmanager
async def lifespan(app):
    try:
        api_logger.info("Connecting to database...")
        db_manager.connect()
        yield
        db_manager.close()
    except Exception as e:
        api_logger.error(f"Error during startup: {e}")
    finally:
        api_logger.info("Closing database connection...")


# ------------------------------
# App Initialization
# ------------------------------
app = FastAPI(lifespan=lifespan, root_path="/api/v1")


# ------------------------------
# Application Exception Handler
# ------------------------------
@app.exception_handler(BaseAPIException)
async def app_execution_handler(request, exc):
    api_error = DefaultApiErrorResponse(
        status_code=exc.status_code,
        message=exc.message
    )
    return JSONResponse(status_code=exc.status_code, content=api_error.__dict__)

# ------------------------------
# Add Routes
# ------------------------------
app.include_router(user_router)

