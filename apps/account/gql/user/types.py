import graphene
from graphene_django import DjangoObjectType

from apps.account.models import User
from apps.account.gql.user.enums import UserGenderENUM

class UserFilterType(graphene.InputObjectType):
    """
    Input type for filtering users.
    """
    is_author = graphene.Boolean(description="Filter users by their author status.")

class AvatarType(graphene.ObjectType):
    """
    Object type for user avatars.
    """
    small = graphene.String(description="URL of the small-sized avatar image.")
    medium = graphene.String(description="URL of the medium-sized avatar image.")
    large = graphene.String(description="URL of the large-sized avatar image.")

class UserQueryType(DjangoObjectType):
    """
    Query type for retrieving user data.
    """
    class Meta:
        model = User
        exclude = ["last_login", "password", "is_staff", "is_superuser", "date_joined", "is_active", "author"]

    avatar = graphene.Field(AvatarType, description="User's avatar images.")
    def resolve_avatar(root, info):
        """
        Resolve the user's avatar images.
        """
        return {
            "small": root.avatar.small_image.url,
            "medium": root.avatar.medium_image.url,
            "large": root.avatar.large_image.url,
        }

class UserListType(graphene.ObjectType):
    """
    Object type for a list of users.
    """
    data = graphene.List(UserQueryType, description="List of users.")
    page_count = graphene.Int(description="Total number of pages for pagination.")
    count = graphene.Int(description="Total number of users in the list.")

class UserEditInputType(graphene.InputObjectType):
    """
    Input type for editing user data.
    """
    base64_image = graphene.Argument(graphene.String, description="Base64-encoded image for updating user avatar.")
    gender = graphene.Field(UserGenderENUM, description="User's gender.")
    password = graphene.Argument(graphene.String, description="User's password for authentication.")
    is_author = graphene.Argument(graphene.Boolean, description="Flag indicating if the user is an author.")
