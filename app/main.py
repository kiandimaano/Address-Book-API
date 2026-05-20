import logging
from fastapi import FastAPI
from app.database import engine, Base
from app.router import addresses

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %s(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Address Book API",
    description="A CRUD API for managing addresses with geolocation support.",
    version="1.0.0"
)

app.include_router(addresses.router)

@app.get("/", tags=["Health"])
def root():
    logger.info("Health check called")
    return {"status": "running", "message": "Address Book API is live"}