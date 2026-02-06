import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from commons.database import db_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(), # Outputs to console
        # logging.FileHandler("app.log") # Optional: save to a file
    ]
)

logger = logging.getLogger(__name__)

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

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}