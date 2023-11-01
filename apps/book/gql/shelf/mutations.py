import graphene
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from apps.book.gql.shelf.types import BookShelfInputType
from apps.book.gql.shelf.types import ChangeBookShelfInputType
from apps.book.models import Book
from apps.book.models import BookShelf
from apps.book.models import Shelf
from helpers import http_code
from helpers.generic_types import ResponseBase


class AddBookToShelf(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(
            BookShelfInputType,
            description="Input data for adding a book to a shelf.",
        )

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):
        """
        Mutate to add a book to a user's shelf.

        Args:
            data (BookShelfInputType): Input data for adding a book to a shelf.

        Returns:
            ResponseBase: Response indicating the success or failure of adding the book to the shelf.
        """

        user = info.context.user
        book = Book.objects.filter(id=data.get("book_id")).first()
        shelf = Shelf.objects.filter(Q(name=getattr(data["shelf_name"], "name", data.get("shelf_name"))) & Q(user=user)).first()

        if book and shelf:
            obj = BookShelf(user=user, book=book, shelf=shelf)
            obj.save()

            return ResponseBase(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("Book added to shelf successfully!"),
            )

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("Operation failed!"),
            )


class RemoveBookFromShelf(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(
            BookShelfInputType,
            description="Input data for removing a book from a shelf.",
        )

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):
        """
        Mutate to remove a book from a user's shelf.

        Args:
            data (BookShelfInputType): Input data for removing a book from a shelf.

        Returns:
            ResponseBase: Response indicating the success or failure of removing the book from the shelf.
        """

        user = info.context.user
        book = Book.objects.filter(id=data.get("book_id")).first()
        shelf = Shelf.objects.filter(name=getattr(data["shelf_name"], "name", data.get("shelf_name")), user=user).first()

        if book and shelf:
            BookShelf.objects.filter(user=user, book=book, shelf=shelf).delete()

            return ResponseBase(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("Book removed from shelf successfully!"),
            )

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("Operation failed!"),
            )


class ChangeBookFromShelf(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(
            ChangeBookShelfInputType,
            description="Input data for changing a book from one shelf to another.",
        )

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):
        """
        Mutate to change a book from one shelf to another on a user's shelf list.

        Args:
            data (ChangeBookShelfInputType): Input data for changing a book from one shelf to another.

        Returns:
            ResponseBase: Response indicating the success or failure of changing the book's shelf.
        """

        user = info.context.user
        book = Book.objects.filter(id=data.get("book_id")).first()
        from_shelf = Shelf.objects.filter(name=getattr(data["from_shelf"], "name", data.get("from_shelf")), user=user).first()
        to_shelf = Shelf.objects.filter(name=getattr(data["to_shelf"], "name", data.get("to_shelf")), user=user).first()

        if book and from_shelf and to_shelf:
            with transaction.atomic():
                BookShelf.objects.filter(user=user, book=book, shelf=from_shelf).delete()
                obj = BookShelf(user=user, book=book, shelf=to_shelf)
                obj.save()

            return ResponseBase(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("Book changed from shelf successfully!"),
            )

        else:
            return ResponseBase(
                status=http_code.HTTP_406_NOT_ACCEPTABLE,
                status_code=http_code.HTTP_406_NOT_ACCEPTABLE_CODE,
                message=_("Operation failed!"),
            )
