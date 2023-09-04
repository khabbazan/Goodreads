from django.http import JsonResponse

def rate_limit_exception_view(request, *args, **kwargs):
    message = "Too many requested, try later."

    response_data = {
        'message': message,
        'status': 'error',
    }
    return JsonResponse(response_data, status=429)
