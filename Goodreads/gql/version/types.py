import graphene
from graphene.types import generic


class BackendVersion(graphene.ObjectType):
    """
    Represents the backend version information.
    """

    current_version = graphene.String(description="The current version of the backend.")
    build_number = graphene.String(description="The build number of the backend.")
    features = generic.GenericScalar(description="A generic scalar field to store additional features.")


class FrontendVersion(graphene.ObjectType):
    """
    Represents the frontend version information.
    """

    current_version = graphene.String(description="The current version of the frontend.")
    build_number = graphene.String(description="The build number of the frontend.")
    features = generic.GenericScalar(description="A generic scalar field to store additional features.")


class VersionType(graphene.Union):
    """
    Represents a union type for dynamic outputs in mutations.
    This union type can hold either BackendVersion or FrontendVersion objects.
    """

    class Meta:
        types = (
            BackendVersion,
            FrontendVersion,
        )
