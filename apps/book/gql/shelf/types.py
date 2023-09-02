import graphene
from graphene_django import DjangoObjectType

from apps.account.models import User
from apps.book.models import Book
from apps.book.models import Shelf
from apps.book.models import BookShelf
from apps.book.gql.shelf.enums import ShelfENUM



class UserShelfQueryType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["id", "phone_number", "gender"]

class BookShelfQueryType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ["id", "title", "ISBN", "description"]

class ShelfQueryType(DjangoObjectType):
    class Meta:
        model = Shelf
        fields = ["id"]

    name = graphene.String()
    def resolve_name(root, info):
        return root.name

    display_name = graphene.String()
    def resolve_display_name(root, info):
        return root.get_name_display()


class UserShelfListQueryType(DjangoObjectType):
    class Meta:
        model = BookShelf
        fields = ["id", "user", "book", "shelf"]

    user = graphene.Field(UserShelfQueryType)
    book = graphene.Field(BookShelfQueryType)
    shelf = graphene.Field(ShelfQueryType)


class BookShelfInputType(graphene.InputObjectType):
    book_id = graphene.Argument(graphene.ID, required=True)
    shelf_name = graphene.Argument(ShelfENUM, required=True)

class ChangeBookShelfInputType(graphene.InputObjectType):
    book_id = graphene.Argument(graphene.ID, required=True)
    from_shelf = graphene.Argument(ShelfENUM, required=True)
    to_shelf = graphene.Argument(ShelfENUM, required=True)
