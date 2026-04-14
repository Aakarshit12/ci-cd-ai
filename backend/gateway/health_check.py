import asyncio
import logging
import urllib.request
from urllib.error import URLError, HTTPError

from app.core.cache import redis_client
from app.core.database import SessionLocal
from gateway.models import RegisteredService

logger = logging.getLogger("health_check")

def check_url_health(url: str) -> bool:
    """Synchronous health check using stdlib."""
    health_endpoint = url.rstrip("/") + "/health"
    try:
        response = urllib.request.urlopen(health_endpoint, timeout=5)
        return response.getcode() == 200
    except (URLError, HTTPError):
        return False

async def health_check_task():
    logger.info("Starting background health check task...")
    while True:
        try:
            # Run the blocking DB call in a thread pool (using thread fallback for simplicity)
            await asyncio.to_thread(_perform_health_checks)
        except Exception as e:
            logger.error(f"Error in health check task: {e}")
        
        await asyncio.sleep(30)

def _perform_health_checks():
    db = SessionLocal()
    try:
        services = db.query(RegisteredService).filter(RegisteredService.is_active == True).all()
        for service in services:
            for url in service.upstream_urls:
                is_healthy = check_url_health(url)
                redis_key = f"gateway:health:{service.id}:{url}"
                if is_healthy:
                    redis_client.set(redis_key, "1", ex=60) # expires slightly after next check
                else:
                    redis_client.set(redis_key, "0", ex=60)
    finally:
        db.close()

def start_health_check_task():
    asyncio.create_task(health_check_task())
