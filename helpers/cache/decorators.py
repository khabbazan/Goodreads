from functools import wraps
from django.core.cache import cache

def query_cache(cache_key, timeout=3600):
    """
    A decorator to cache the results of a GraphQL query function.

    This decorator can be applied to a resolver function in a Django GraphQL view.
    It caches the results of the query function in Django's cache system, with a
    cache key based on the provided `cache_key_prefix` and the query itself.

    Args:
        cache_key (str): A prefix for the cache key, usually related to
            the specific GraphQL query or resolver.
        timeout (int, optional): The cache timeout in seconds. Default is 3600 (1 hour).

    Returns:
        callable: A wrapped GraphQL resolver function.
    """

    def decorator(query_function):
        @wraps(query_function)
        def wrapper(root, info, **kwargs):
            """
            Wrapper function for caching query results.

            Args:
                root: The root value passed to the resolver.
                info: The GraphQL resolve info.
                **kwargs: Keyword arguments specific to the query function.

            Returns:
                The result of the query function.
            """
            query = info.operation.selection_set or info.operation.operation
            result = cache.get(cache_key)

            if result is None:
                result = query_function(root, info, **kwargs)
                cache.set(cache_key, result, timeout=timeout)

            return result

        return wrapper

    return decorator

def expire_cache_keys(cache_keys):
    """
    A decorator to expire cache keys after executing a mutation function.

    This decorator can be applied to a mutation resolver function in a Django GraphQL view.
    It deletes specified cache keys after the mutation function is executed.

    Args:
        cache_keys (list): A list of cache keys to be deleted after the mutation.

    Returns:
        callable: A wrapped mutation resolver function.
    """

    def decorator(mutation_function):
        @wraps(mutation_function)
        def wrapper(*args, **kwargs):
            """
            Wrapper function for expiring cache keys after mutation execution.

            Args:
                *args: Positional arguments passed to the mutation function.
                **kwargs: Keyword arguments passed to the mutation function.

            Returns:
                The result of the mutation function.
            """
            result = mutation_function(*args, **kwargs)

            if cache_keys:
                for cache_key in cache_keys:
                    cache.delete(cache_key)

            return result

        return wrapper

    return decorator

