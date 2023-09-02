import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required
from django.db import transaction
from django.db.models import Q

from helpers import http_code
from helpers.generic_types import ResponseBase
from apps.book.gql.shelf.types import BookShelfInputType
from apps.book.gql.shelf.types import ChangeBookShelfInputType
from apps.book.models import Book
from apps.book.models import Shelf
from apps.book.models import BookShelf


class AddBookToShelf(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(BookShelfInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        book = Book.objects.filter(id=data.get("book_id")).first()
        shelf = Shelf.objects.filter(
            Q(name=getattr(data["shelf_name"], "name", data.get("shelf_name"))) & Q(user=user)
        ).first()

        if book and shelf:
            obj = BookShelf(user=user, book=book, shelf=shelf)
            obj.save()

            return ResponseBase(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("book added to shelf successfully!"),
            )

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("operation failed!"),
            )


class RemoveBookFromShelf(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(BookShelfInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        book = Book.objects.filter(id=data.get("book_id")).first()
        shelf = Shelf.objects.filter(
            name=getattr(data["shelf_name"], "name", data.get("shelf_name")),
            user=user
        ).first()

        if book and shelf:
            BookShelf.objects.filter(user=user, book=book, shelf=shelf).delete()

            return ResponseBase(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("book removed from shelf successfully!"),
            )

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("operation failed!"),
            )

class ChangeBookFromShelf(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(ChangeBookShelfInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        book = Book.objects.filter(id=data.get("book_id")).first()
        from_shelf = Shelf.objects.filter(
            name=getattr(data["from_shelf"], "name", data.get("from_shelf")),
            user=user
        ).first()
        to_shelf = Shelf.objects.filter(
            name=getattr(data["to_shelf"], "name", data.get("to_shelf")),
            user=user
        ).first()

        if book and from_shelf and to_shelf:
            with transaction.atomic():
                BookShelf.objects.filter(user=user, book=book, shelf=from_shelf).delete()
                obj = BookShelf(user=user, book=book, shelf=to_shelf)
                obj.save()

            return ResponseBase(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("book changed from shelf successfully!"),
            )

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("operation failed!"),
            )
