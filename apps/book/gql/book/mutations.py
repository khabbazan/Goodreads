import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required
from django.db import transaction
from django.db.models import Q

from apps.book.gql.book.types import BookInputType
from apps.book.gql.book.types import BookEditInputType
from apps.account.models import Author
from apps.book.models import BookAuthor
from apps.book.models import Book
from apps.book.models import Tag
from helpers import http_code
from helpers.generic_types import ResponseBase
from helpers.cache.decorators import expire_cache_keys

class BookAdd(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(BookInputType)

    Output = ResponseBase

    @expire_cache_keys(["book.list"])
    @login_required
    def mutate(self, info, data):

        author_data = data.pop("author", {})
        author = Author.objects.filter(
            Q(id=author_data.get('pk')) | Q(user__phone_number=author_data.get("phone_number"))
        ).first()


        tags = [item.name for item in data.pop("tags", [])]
        tags = Tag.objects.filter(name__in=tags)


        Book.clean_fields(**data)

        with transaction.atomic():
            book = Book(**data)

            book_author = BookAuthor(book=book, author=author)
            book.save()
            book_author.save()
            book.tags.add(*tags)

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("book added successfully!"),
        )


class BookEdit(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(BookEditInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        pk = data.pop("pk")
        user = info.context.user

        tags = [item.name for item in data.pop("tags", [])]
        tags = Tag.objects.filter(name__in=tags)

        Book.clean_fields(**data)

        book = Book.objects.filter(id=pk, authors__author__user=user).first()

        if book:
            with transaction.atomic():
                Book.objects.filter(id=book.id).update(**data)
                if tags:
                    book.tags.clear()
                    book.tags.add(*tags)

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("You are not the author of this book"),
            )

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Changed successfully!"),
        )
