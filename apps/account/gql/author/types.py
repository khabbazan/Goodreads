import graphene
from graphene_django import DjangoObjectType

from apps.account.models import Author

# Define an input object type for filtering authors.
class AuthorFilterType(graphene.InputObjectType):
    """
    Input type for filtering authors.
    """
    is_active = graphene.Boolean(description="Filter authors by their active status.")

# Define a query object type for retrieving author data.
class AuthorQueryType(DjangoObjectType):
    """
    Query type for retrieving author data.
    """
    class Meta:
        model = Author
        exclude = ["last_login", "password", "is_staff", "is_superuser", "date_joined"]

# Define an object type for a list of authors.
class AuthorListType(graphene.ObjectType):
    """
    Object type for a list of authors.
    """
    data = graphene.List(AuthorQueryType, description="List of authors.")
    page_count = graphene.Int(description="Total number of pages for pagination.")
    count = graphene.Int(description="Total number of authors in the list.")

# Define an input object type for editing author data.
class AuthorEditInputType(graphene.InputObjectType):
    """
    Input type for editing author data.
    """
    first_name = graphene.Argument(graphene.String, description="Author's first name.")
    last_name = graphene.Argument(graphene.String, description="Author's last name.")
