import math

import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from apps.account.gql.relation.types import UserFollowerListType
from apps.account.gql.relation.types import UserFollowingListType
from helpers.generic_types import PageType


class UserFollowerList(graphene.ObjectType):

    user_follower_list = graphene.Field(
        UserFollowerListType,
        search=graphene.String(description="Search for user followers based on a keyword."),
        page=graphene.Argument(PageType, description="Paginate through the list of user followers."),
    )

    @login_required
    def resolve_user_follower_list(self, info, **kwargs):
        """
        Resolve the user_follower_list field to retrieve a list of user followers.

        Args:
            search (str, optional): Search keyword for user followers. Defaults to an empty string.
            page (PageType, optional): Pagination settings. Defaults to page 1 with 10 items per page.

        Returns:
            UserFollowerListType: A paginated list of user followers.
        """

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
        search=graphene.String(description="Search for users following based on a keyword."),
        page=graphene.Argument(PageType, description="Paginate through the list of users following."),
    )

    @login_required
    def resolve_user_following_list(self, info, **kwargs):
        """
        Resolve the user_following_list field to retrieve a list of users following.

        Args:
            search (str, optional): Search keyword for users following. Defaults to an empty string.
            page (PageType, optional): Pagination settings. Defaults to page 1 with 10 items per page.

        Returns:
            UserFollowingListType: A paginated list of users following.
        """

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
