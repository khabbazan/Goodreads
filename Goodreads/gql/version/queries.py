import graphene
from django.conf import settings

from Goodreads.gql.version.types import BackendVersion
from Goodreads.gql.version.types import VersionType


class VersionDetail(graphene.ObjectType):
    """
    Represents version details for the application.
    """

    version = graphene.Field(VersionType, description="A GraphQL field containing version information.")

    def resolve_version(self, info, **kwargs):
        """
        Resolves and provides the version information.
        """
        return BackendVersion(
            current_version=settings.VERSION,
            build_number=settings.BUILD_NUMBER,
        )
