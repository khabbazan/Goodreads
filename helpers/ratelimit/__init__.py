from django.conf import settings
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit

def rate_limit_exception_view(request, *args, **kwargs):
    message = "Too many requested, try later."

    response_data = {
        'message': message,
        'status': 'error',
    }
    return JsonResponse(response_data, status=429)


def rate_limit_custom_decorate(request):
    if not settings.DEBUG:
        return ratelimit(**settings.RATELIMIT_CONFIGS)(request)
    return request
