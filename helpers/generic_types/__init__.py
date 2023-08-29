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


class ResponseUnion(graphene.Union):
    """
    use for dynamic outputs in mutations.
    """

    class Meta:
        types = (
            ResponseWithToken,
            ResponseBase,
        )

class PageType(graphene.InputObjectType):
    page_size = graphene.Int()
    page_number = graphene.Int()
