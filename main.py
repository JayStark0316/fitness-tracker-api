import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import JSONResponse

from commons.database import db_manager
from commons.exceptions.base_api_exception_handler import BaseAPIException
from commons.exceptions.default_error_api_response import DefaultApiErrorResponse


# ------------------------------
# Logging Configuration
# ------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(), # Outputs to console
        # logging.FileHandler("app.log") # Optional: save to a file
    ]
)

logger = logging.getLogger(__name__)

# ------------------------------
# Life Span Handler
# ------------------------------
@asynccontextmanager
async def lifespan(app):
    try:
        logger.info("Connecting to database...")
        db_manager.connect()
        yield
        db_manager.close()
    except Exception as e:
        logger.error(f"Error during startup: {e}")
    finally:
        logger.info("Closing database connection...")


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

