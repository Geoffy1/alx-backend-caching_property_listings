from django. core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieves and logs Redis cache hit/miss metrics.
    """
    try:
        # Get the underlying Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get info about the server, which includes keyspace stats
        info = redis_conn.info()
        
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)

        total_requests = keyspace_hits + keyspace_misses

        if total_requests > 0:
            hit_ratio = keyspace_hits / total_requests
        else:
            hit_ratio = 0.0

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': hit_ratio,
        }
        
        logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, Hit Ratio={hit_ratio:.2f}")
        
        return metrics

    except Exception as e:
        logger.error(f"Error getting Redis metrics: {e}")
        return {}
# We can also call this function from somewhere, like the view,
# to see the metrics in the server logs

def get_all_properties():
    """
    Fetches all properties from the database with low-level caching.
    """
    # Define a cache key
    cache_key = 'all_properties'
    # Define the cache duration (in seconds)
    cache_timeout = 3600  # 1 hour

    # Try to get the data from the cache
    properties = cache.get(cache_key)

    if properties is None:
        # Data not in cache, fetch from database
        print("Fetching properties from database and setting cache...")
        properties = list(Property.objects.all())  # convert to list to force evaluation
        
        # Store the queryset in the cache
        cache.set(cache_key, properties, cache_timeout)
    else:
        print("Properties retrieved from cache.")

    return properties
