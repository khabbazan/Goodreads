import math
import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from apps.account.gql.author.types import AuthorListType
from apps.account.gql.author.types import AuthorFilterType
from apps.account.gql.author.types import AuthorQueryType
from helpers.generic_types import PageType
from apps.account.models import Author


class AuthorList(graphene.ObjectType):

    author_list = graphene.Field(
        AuthorListType,
        search=graphene.String(),
        filter=graphene.Argument(AuthorFilterType),
        page=graphene.Argument(PageType),
    )

    @login_required
    def resolve_author_list(self, info, **kwargs):
        search = kwargs.get("search", "")
        filter = kwargs.get("filter", "")
        page = kwargs.get("page", {"page_size": 10, "page_number": 1})

        res = Author.objects.search(search)
        if filter:
            filter_is_active = filter.get('is_active')
            if filter_is_active is not None:
                res = res.filter(user__is_author=filter_is_active)


        page_number = page.get("page_number")
        page_size = page.get("page_size")

        paginator = Paginator(res, page_size)
        page_count = math.ceil(res.count() / int(page.get("page_size")))
        count = res.count()

        return AuthorListType(data=paginator.page(page_number), page_count=page_count, count=count)


class AuthorDetail(graphene.ObjectType):

    author_detail = graphene.Field(
        AuthorQueryType,
        pk=graphene.ID(required=True),
    )

    def resolve_author_detail(self, info, pk):
        return Author.objects.filter(pk=pk).first()
