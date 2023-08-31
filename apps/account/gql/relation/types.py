import graphene
from graphene_django import DjangoObjectType

from apps.account.models import Relation

class UserFollowerQueryType(DjangoObjectType):
    class Meta:
        model = Relation
        fields = ["follower", "following_on"]

class UserFollowerListType(graphene.ObjectType):
    data = graphene.List(UserFollowerQueryType)
    page_count = graphene.Int()
    count = graphene.Int()

class UserFollowingQueryType(DjangoObjectType):
    class Meta:
        model = Relation
        fields = ["following", "following_on"]

class UserFollowingListType(graphene.ObjectType):
    data = graphene.List(UserFollowingQueryType)
    page_count = graphene.Int()
    count = graphene.Int()

class FollowInputType(graphene.InputObjectType):
    id = graphene.Argument(graphene.ID)
    phone_number = graphene.Argument(graphene.String)
