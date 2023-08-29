import math
import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from apps.account.gql.user.types import UserListType
from apps.account.gql.user.types import UserFilterType
from apps.account.gql.user.types import UserQueryType
from helpers.generic_types import PageType
from apps.account.models import User


class UserList(graphene.ObjectType):

    user_list = graphene.Field(
        UserListType,
        search=graphene.String(),
        filter=graphene.Argument(UserFilterType),
        page=graphene.Argument(PageType),
    )

    @login_required
    def resolve_user_list(self, info, **kwargs):
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
        pk=graphene.ID(required=True),
    )

    def resolve_user_detail(self, info, pk):
        return User.objects.filter(pk=pk).first()
