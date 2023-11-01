import graphene
from graphene_django import DjangoObjectType

from apps.book.gql.tag.enums import BookTagENUM
from apps.book.models import Book
from apps.book.models import BookAuthor


class BookAuthorInputType(graphene.InputObjectType):
    """
    Input type for book authors.
    """

    pk = graphene.Argument(graphene.ID, description="ID of the book author.")
    phone_number = graphene.Argument(graphene.String, description="Phone number of the book author.")


class BookAuthorQueryType(DjangoObjectType):
    """
    Query type for retrieving book authors.
    """

    class Meta:
        model = BookAuthor
        fields = ["author"]


class BookInputType(graphene.InputObjectType):
    """
    Input type for creating or updating books.
    """

    author = graphene.Field(BookAuthorInputType, required=True, description="Author of the book.")
    ISBN = graphene.Argument(graphene.String, required=True, description="ISBN of the book.")
    title = graphene.Argument(graphene.String, required=True, description="Title of the book.")
    tags = graphene.Argument(graphene.List(BookTagENUM), description="Tags associated with the book.")
    description = graphene.Argument(graphene.String, description="Description of the book.")


class BookQueryType(DjangoObjectType):
    """
    Query type for retrieving book data.
    """

    class Meta:
        model = Book
        fields = "__all__"

    authors = graphene.List(BookAuthorQueryType, description="List of authors of the book.")

    def resolve_authors(root, info):
        """
        Resolve the authors of the book.
        """
        return root.authors.all()


class BookListType(graphene.ObjectType):
    """
    Object type for a list of books.
    """

    data = graphene.List(BookQueryType, description="List of books.")
    page_count = graphene.Int(description="Total number of pages for pagination.")
    count = graphene.Int(description="Total number of books in the list.")


class BookFilterType(graphene.InputObjectType):
    """
    Input type for filtering books.
    """

    is_active = graphene.Boolean(description="Filter books by their active status.")
    tags = graphene.Argument(graphene.List(BookTagENUM), description="Filter books by tags.")


class BookEditInputType(graphene.InputObjectType):
    """
    Input type for editing book data.
    """

    pk = graphene.Argument(graphene.ID, required=True, description="ID of the book to edit.")
    ISBN = graphene.Argument(graphene.String, description="ISBN of the book.")
    title = graphene.Argument(graphene.String, description="Title of the book.")
    description = graphene.Argument(graphene.String, description="Description of the book.")
    tags = graphene.Argument(graphene.List(BookTagENUM), description="Tags associated with the book.")
    is_active = graphene.Argument(graphene.Boolean, description="Flag indicating if the book is active.")
