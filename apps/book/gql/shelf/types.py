import graphene
from graphene_django import DjangoObjectType

from apps.account.models import User
from apps.book.models import Book
from apps.book.models import Shelf
from apps.book.models import BookShelf
from apps.book.gql.shelf.enums import ShelfENUM

class UserShelfQueryType(DjangoObjectType):
    """
    Query type for retrieving user shelf data.
    """
    class Meta:
        model = User
        fields = ["id", "phone_number", "gender"]

class BookShelfQueryType(DjangoObjectType):
    """
    Query type for retrieving bookshelf data.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "ISBN", "description"]

class ShelfQueryType(DjangoObjectType):
    """
    Query type for retrieving shelf data.
    """
    class Meta:
        model = Shelf
        fields = ["id"]

    name = graphene.String(description="Name of the shelf.")
    def resolve_name(root, info):
        """
        Resolve the name of the shelf.
        """
        return root.name

    display_name = graphene.String(description="Display name of the shelf.")
    def resolve_display_name(root, info):
        """
        Resolve the display name of the shelf.
        """
        return root.get_name_display()

class UserShelfListQueryType(DjangoObjectType):
    """
    Query type for retrieving user shelf list data.
    """
    class Meta:
        model = BookShelf
        fields = ["id", "user", "book", "shelf"]

    user = graphene.Field(UserShelfQueryType, description="User associated with the shelf.")
    book = graphene.Field(BookShelfQueryType, description="Book associated with the shelf.")
    shelf = graphene.Field(ShelfQueryType, description="Shelf associated with the user and book.")

class BookShelfInputType(graphene.InputObjectType):
    """
    Input type for adding a book to a shelf.
    """
    book_id = graphene.Argument(graphene.ID, required=True, description="ID of the book to add to the shelf.")
    shelf_name = graphene.Argument(ShelfENUM, required=True, description="Name of the shelf to add the book to.")

class ChangeBookShelfInputType(graphene.InputObjectType):
    """
    Input type for changing a book's shelf.
    """
    book_id = graphene.Argument(graphene.ID, required=True, description="ID of the book to move to a new shelf.")
    from_shelf = graphene.Argument(ShelfENUM, required=True, description="Name of the current shelf of the book.")
    to_shelf = graphene.Argument(ShelfENUM, required=True, description="Name of the target shelf for the book.")
