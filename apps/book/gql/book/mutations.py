import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required
from django.db import transaction
from django.db.models import Q

from helpers import http_code
from helpers.generic_types import ResponseBase
from apps.book.gql.book.types import BookInputType
from apps.book.gql.book.types import BookEditInputType
from apps.account.models import Author
from apps.book.models import BookAuthor
from apps.book.models import Book


class BookAdd(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(BookInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        author_data = data.pop("author", {})
        author = Author.objects.filter(
            Q(id=author_data.get('pk')) | Q(user__phone_number=author_data.get("phone_number"))
        ).first()

        with transaction.atomic():
            book = Book(**data)
            book_author = BookAuthor(book=book, author=author)
            book.save()
            book_author.save()

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

        book = Book.objects.filter(id=pk, authors__author__user=user).first()

        if book:
            Book.objects.filter(id=pk).update(**data)

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
