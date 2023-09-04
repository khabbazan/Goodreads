import math
import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from apps.book.gql.book.types import BookListType
from apps.book.gql.book.types import BookQueryType
from apps.book.gql.book.types import BookFilterType
from helpers.generic_types import PageType
from apps.book.models import Book


class BookList(graphene.ObjectType):

    book_list = graphene.Field(
        BookListType,
        search=graphene.String(),
        filter=graphene.Argument(BookFilterType),
        page=graphene.Argument(PageType),
    )

    @login_required
    def resolve_book_list(self, info, **kwargs):
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
        pk=graphene.ID(required=True),
    )

    def resolve_book_detail(self, info, pk):
        return Book.objects.filter(pk=pk).first()
