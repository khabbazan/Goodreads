import graphene
from graphene_django import DjangoObjectType

from apps.account.models import Author


class AuthorFilterType(graphene.InputObjectType):
    is_active = graphene.Boolean()

class AuthorQueryType(DjangoObjectType):
    class Meta:
        model = Author
        exclude = ["last_login", "password", "is_staff", "is_superuser", "date_joined"]

class AuthorListType(graphene.ObjectType):
    data = graphene.List(AuthorQueryType)
    page_count = graphene.Int()
    count = graphene.Int()

class AuthorEditInputType(graphene.InputObjectType):
    first_name = graphene.Argument(graphene.String)
    last_name = graphene.Argument(graphene.String)
