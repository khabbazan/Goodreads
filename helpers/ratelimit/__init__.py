from django.conf import settings
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit

def rate_limit_exception_view(request, *args, **kwargs):
    """
    View to handle rate limiting exceptions.

    This view is used to handle rate limiting exceptions and return an error response when the rate limit is exceeded.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing an error message and status code 429 (Too Many Requests).
    """
    message = "Too many requests, please try again later."

    response_data = {
        'message': message,
        'status': 'error',
    }
    return JsonResponse(response_data, status=429)

def rate_limit_custom_decorate(request):
    """
    Custom rate limiting decorator.

    This function applies rate limiting to the view function based on the settings in settings.RATELIMIT_CONFIGS.
    It checks if the application is in debug mode, and if not, applies rate limiting to the request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The original request or a rate-limited response based on the application's debug mode.
    """
    if not settings.DEBUG:
        return ratelimit(**settings.RATELIMIT_CONFIGS)(request)
    return request
