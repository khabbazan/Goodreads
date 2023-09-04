import graphene
from graphene_django import DjangoObjectType

from apps.account.models import User
from apps.account.gql.user.enums import UserGenderENUM


class UserFilterType(graphene.InputObjectType):
    is_author = graphene.Boolean()

class AvatarType(graphene.ObjectType):
    small = graphene.String()
    medium = graphene.String()
    large = graphene.String()

class UserQueryType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["last_login", "password", "is_staff", "is_superuser", "date_joined", "is_active", "author"]

    avatar = graphene.Field(AvatarType)
    def resolve_avatar(root, info):
        return {
            "small": root.avatar.small_image.url,
            "medium": root.avatar.medium_image.url,
            "large": root.avatar.large_image.url,
        }

class UserListType(graphene.ObjectType):
    data = graphene.List(UserQueryType)
    page_count = graphene.Int()
    count = graphene.Int()

class UserEditInputType(graphene.InputObjectType):
    base64_image = graphene.Argument(graphene.String)
    gender = graphene.Field(UserGenderENUM)
    password = graphene.Argument(graphene.String)
    is_author = graphene.Argument(graphene.Boolean)
