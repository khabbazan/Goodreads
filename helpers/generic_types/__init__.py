import graphene
from graphene.types import generic


class ResponseBase(graphene.ObjectType):
    status = graphene.String()
    status_code = graphene.Int()
    message = graphene.String()
    metadata = generic.GenericScalar()


class ResponseWithToken(graphene.ObjectType):
    status = graphene.String()
    status_code = graphene.Int()
    message = graphene.String()
    token = graphene.String()
    refresh_token = graphene.String()
    metadata = generic.GenericScalar()


class ResponseType(graphene.Union):
    """
    use for dynamic outputs in mutations.
    """

    class Meta:
        types = (
            ResponseWithToken,
            ResponseBase,
        )

class PageType(graphene.InputObjectType):
    page_size = graphene.Int(default=10)
    page_number = graphene.Int(default=1)
