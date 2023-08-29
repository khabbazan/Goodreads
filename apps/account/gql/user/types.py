import graphene
from graphene_django import DjangoObjectType

from apps.account.models import User


class UserFilterType(graphene.InputObjectType):
    is_author = graphene.Boolean()

class UserQueryType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["last_login", "password", "is_staff", "is_superuser", "date_joined", "is_active"]

class UserListType(graphene.ObjectType):
    data = graphene.List(UserQueryType)
    page_count = graphene.Int()
    count = graphene.Int()

class UserEditInputType(graphene.InputObjectType):
    password = graphene.Argument(graphene.String)
