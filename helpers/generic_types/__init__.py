import graphene
from graphene.types import generic

class ResponseBase(graphene.ObjectType):
    """
    Represents a basic response object.

    Fields:
        - status (str): The status of the response.
        - status_code (int): The HTTP status code of the response.
        - message (str): A message associated with the response.
        - metadata (GenericScalar): Additional metadata associated with the response.
    """
    status = graphene.String()
    status_code = graphene.Int()
    message = graphene.String()
    metadata = generic.GenericScalar()

class ResponseWithToken(graphene.ObjectType):
    """
    Represents a response object with authentication tokens.

    Fields:
        - status (str): The status of the response.
        - status_code (int): The HTTP status code of the response.
        - message (str): A message associated with the response.
        - token (str): An authentication token.
        - refresh_token (str): A refresh token.
        - metadata (GenericScalar): Additional metadata associated with the response.
    """
    status = graphene.String()
    status_code = graphene.Int()
    message = graphene.String()
    token = graphene.String()
    refresh_token = graphene.String()
    metadata = generic.GenericScalar()

class ResponseUnion(graphene.Union):
    """
    Represents a union of response types for dynamic outputs in mutations.

    Types:
        - ResponseWithToken: A response with authentication tokens.
        - ResponseBase: A basic response.

    Usage:
        Use this union for dynamic outputs in mutations.
    """
    class Meta:
        types = (
            ResponseWithToken,
            ResponseBase,
        )

class PageType(graphene.InputObjectType):
    """
    Represents an input object for specifying pagination parameters.

    Fields:
        - page_size (int): The number of items per page.
        - page_number (int): The page number.
    """
    page_size = graphene.Int()
    page_number = graphene.Int()
