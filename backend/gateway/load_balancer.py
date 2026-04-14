from typing import List, Optional
from uuid import UUID

from app.core.cache import redis_client

class NoHealthyUpstreamError(Exception):
    """Raised when no healthy upstreams are available for a service."""
    pass

def get_healthy_upstreams(service_id: str, upstream_urls: List[str]) -> List[str]:
    """Filters upstream URLs based on their health status in Redis."""
    healthy_urls = []
    for url in upstream_urls:
        health_key = f"gateway:health:{service_id}:{url}"
        status = redis_client.get(health_key)
        # If status is None (not checked yet) or '1' (healthy), include it.
        if status is None or status == "1":
            healthy_urls.append(url)
    return healthy_urls

def get_next_upstream(service_id: UUID, all_upstream_urls: List[str]) -> str:
    """
    Returns the next healthy upstream URL using Redis for atomic Round Robin.
    """
    if not all_upstream_urls:
        raise NoHealthyUpstreamError("Service has no upstream URLs configured.")

    service_id_str = str(service_id)
    healthy_urls = get_healthy_upstreams(service_id_str, all_upstream_urls)
    
    if not healthy_urls:
        raise NoHealthyUpstreamError("No healthy upstreams available.")

    # Atomic increment using Redis INCR
    index_key = f"gateway:lb:{service_id_str}:index"
    current_index = redis_client.incr(index_key)
    
    # We use (current_index - 1) modulo the number of healthy URLs
    # so that the first call is index 0.
    selected_url = healthy_urls[(current_index - 1) % len(healthy_urls)]
    return selected_url
