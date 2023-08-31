import math

import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from helpers.generic_types import PageType
from apps.account.gql.relation.types import UserFollowerListType
from apps.account.gql.relation.types import UserFollowingListType


class UserFollowerList(graphene.ObjectType):

    user_follower_list = graphene.Field(
        UserFollowerListType,
        search=graphene.String(),
        page=graphene.Argument(PageType),
    )

    @login_required
    def resolve_user_follower_list(self, info, **kwargs):

        search = kwargs.get("search", "")
        page = kwargs.get("page", {"page_size": 10, "page_number": 1})
        user = info.context.user

        res = user.followers.all()

        if search:
            res = res.filter(follower__phone_number__contains=search)

        page_number = page.get("page_number")
        page_size = page.get("page_size")

        paginator = Paginator(res, page_size)
        page_count = math.ceil(res.count() / int(page.get("page_size")))
        count = res.count()

        return UserFollowerListType(data=paginator.page(page_number), page_count=page_count, count=count)

class UserFollowingList(graphene.ObjectType):

    user_following_list = graphene.Field(
        UserFollowingListType,
        search=graphene.String(),
        page=graphene.Argument(PageType),
    )

    @login_required
    def resolve_user_following_list(self, info, **kwargs):

        search = kwargs.get("search", "")
        page = kwargs.get("page", {"page_size": 10, "page_number": 1})
        user = info.context.user

        res = user.following.all()

        if search:
            res = res.filter(following__phone_number__contains=search)

        page_number = page.get("page_number")
        page_size = page.get("page_size")

        paginator = Paginator(res, page_size)
        page_count = math.ceil(res.count() / int(page.get("page_size")))
        count = res.count()

        return UserFollowingListType(data=paginator.page(page_number), page_count=page_count, count=count)
