import math
import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from apps.book.gql.book.types import BookListType
from apps.book.gql.book.types import BookQueryType
from apps.book.gql.book.types import BookFilterType
from apps.book.models import Book
from helpers.generic_types import PageType
from helpers.cache.decorators import query_cache

class BookList(graphene.ObjectType):

    book_list = graphene.Field(
        BookListType,
        search=graphene.String(description="Search for books based on a keyword."),
        filter=graphene.Argument(BookFilterType, description="Filter books based on specific criteria."),
        page=graphene.Argument(PageType, description="Paginate through the list of books."),
    )

    @query_cache(cache_key="book.list")
    @login_required
    def resolve_book_list(self, info, **kwargs):
        """
        Resolve the book_list field to retrieve a list of books.

        Args:
            search (str, optional): Search keyword for books. Defaults to an empty string.
            filter (BookFilterType, optional): Filter criteria for books. Defaults to an empty filter.
            page (PageType, optional): Pagination settings. Defaults to page 1 with 10 items per page.

        Returns:
            BookListType: A paginated list of books.
        """
        search = kwargs.get("search", "")
        filter = kwargs.get("filter", "")
        page = kwargs.get("page", {"page_size": 10, "page_number": 1})

        res = Book.objects.search(search)
        if filter:
            filter_is_active = filter.get('is_active')
            if filter_is_active is not None:
                res = res.filter(is_active=filter_is_active)

            tags = filter.get("tags")
            if tags:
                res = res.filter(tags__name__in=tags).distinct()

        page_number = page.get("page_number")
        page_size = page.get("page_size")

        paginator = Paginator(res, page_size)
        page_count = math.ceil(res.count() / int(page.get("page_size")))
        count = res.count()

        return BookListType(data=paginator.page(page_number), page_count=page_count, count=count)


class BookDetail(graphene.ObjectType):

    book_detail = graphene.Field(
        BookQueryType,
        pk=graphene.ID(required=True, description="The unique identifier of the book."),
    )

    def resolve_book_detail(self, info, pk):
        """
        Resolve the book_detail field to retrieve a specific book.

        Args:
            pk (str): The unique identifier of the book.

        Returns:
            BookQueryType: The book with the specified ID.
        """
        return Book.objects.filter(pk=pk).first()
