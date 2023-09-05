import math
import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from apps.account.gql.user.types import UserListType
from apps.account.gql.user.types import UserFilterType
from apps.account.gql.user.types import UserQueryType
from apps.account.models import User
from helpers.generic_types import PageType
from helpers.cache.decorators import query_cache

class UserList(graphene.ObjectType):

    user_list = graphene.Field(
        UserListType,
        search=graphene.String(description="Search for users based on a keyword."),
        filter=graphene.Argument(UserFilterType, description="Filter users based on specific criteria."),
        page=graphene.Argument(PageType, description="Paginate through the list of users."),
    )

    @query_cache(cache_key="user.list")
    @login_required
    def resolve_user_list(self, info, **kwargs):
        """
        Resolve the user_list field to retrieve a list of users.

        Args:
            search (str, optional): Search keyword. Defaults to an empty string.
            filter (UserFilterType, optional): Filter criteria for users. Defaults to an empty filter.
            page (PageType, optional): Pagination settings. Defaults to page 1 with 10 items per page.

        Returns:
            UserListType: A paginated list of users.
        """
        search = kwargs.get("search", "")
        filter = kwargs.get("filter", "")
        page = kwargs.get("page", {"page_size": 10, "page_number": 1})

        res = User.objects.search(search)
        if filter:
            filter_is_author = filter.get('is_author')
            if filter_is_author is not None:
                res = res.filter(is_author=filter_is_author)

        page_number = page.get("page_number")
        page_size = page.get("page_size")

        paginator = Paginator(res, page_size)
        page_count = math.ceil(res.count() / int(page.get("page_size")))
        count = res.count()

        return UserListType(data=paginator.page(page_number), page_count=page_count, count=count)


class UserDetail(graphene.ObjectType):

    user_detail = graphene.Field(
        UserQueryType,
        pk=graphene.ID(required=True, description="The unique identifier of the user."),
    )

    def resolve_user_detail(self, info, pk):
        """
        Resolve the user_detail field to retrieve a specific user.

        Args:
            pk (str): The unique identifier of the user.

        Returns:
            UserQueryType: The user with the specified ID.
        """
        return User.objects.filter(pk=pk).first()
