import math

import graphene
from django.core.paginator import Paginator

from apps.account.gql.author.types import AuthorFilterType
from apps.account.gql.author.types import AuthorListType
from apps.account.gql.author.types import AuthorQueryType
from apps.account.models import Author
from helpers.cache.decorators import query_cache
from helpers.generic_types import PageType


class AuthorList(graphene.ObjectType):

    author_list = graphene.Field(
        AuthorListType,
        search=graphene.String(description="Search for authors based on a keyword."),
        filter=graphene.Argument(AuthorFilterType, description="Filter authors based on specific criteria."),
        page=graphene.Argument(PageType, description="Paginate through the list of authors."),
    )

    @query_cache(cache_key="author.list")
    def resolve_author_list(self, info, **kwargs):
        """
        Resolve the author_list field to retrieve a list of authors.

        Args:
            search (str, optional): Search keyword for authors. Defaults to an empty string.
            filter (AuthorFilterType, optional): Filter criteria for authors. Defaults to an empty filter.
            page (PageType, optional): Pagination settings. Defaults to page 1 with 10 items per page.

        Returns:
            AuthorListType: A paginated list of authors.
        """
        search = kwargs.get("search", "")
        filter = kwargs.get("filter", "")
        page = kwargs.get("page", {"page_size": 10, "page_number": 1})

        res = Author.objects.search(search)
        if filter:
            filter_is_active = filter.get("is_active")
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
        pk=graphene.ID(required=True, description="The unique identifier of the author."),
    )

    def resolve_author_detail(self, info, pk):
        """
        Resolve the author_detail field to retrieve a specific author.

        Args:
            pk (str): The unique identifier of the author.

        Returns:
            AuthorQueryType: The author with the specified ID.
        """
        return Author.objects.filter(pk=pk).first()
