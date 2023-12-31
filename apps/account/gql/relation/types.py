import graphene
from graphene_django import DjangoObjectType

from apps.account.models import Relation


class UserFollowerQueryType(DjangoObjectType):
    """
    Query type for retrieving user followers.
    """

    class Meta:
        model = Relation
        fields = ["follower", "following_on"]


class UserFollowerListType(graphene.ObjectType):
    """
    Object type for a list of user followers.
    """

    data = graphene.List(UserFollowerQueryType, description="List of user followers.")
    page_count = graphene.Int(description="Total number of pages for pagination.")
    count = graphene.Int(description="Total number of user followers in the list.")


class UserFollowingQueryType(DjangoObjectType):
    """
    Query type for retrieving user following.
    """

    class Meta:
        model = Relation
        fields = ["following", "following_on"]


class UserFollowingListType(graphene.ObjectType):
    """
    Object type for a list of user following.
    """

    data = graphene.List(UserFollowingQueryType, description="List of user following.")
    page_count = graphene.Int(description="Total number of pages for pagination.")
    count = graphene.Int(description="Total number of user following in the list.")


class FollowInputType(graphene.InputObjectType):
    """
    Input type for following or unfollowing users.
    """

    id = graphene.Argument(graphene.ID, description="ID of the user to follow or unfollow.")
    phone_number = graphene.Argument(graphene.String, description="Phone number of the user to follow or unfollow.")
