from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from helpers.ratelimit import rate_limit_custom_decorate

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(rate_limit_custom_decorate(GraphQLView.as_view(graphiql=settings.DEBUG)))),
    path(
        "graphql-admin/",
        (user_passes_test(lambda u: u.is_superuser)(GraphQLView.as_view(graphiql=True))),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
