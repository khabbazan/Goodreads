import graphene
from graphene_django import DjangoObjectType

from apps.book.models import Book
from apps.book.models import BookAuthor
from apps.book.gql.tag.enums import BookTagENUM


class BookAuthorInputType(graphene.InputObjectType):
    pk = graphene.Argument(graphene.ID)
    phone_number = graphene.Argument(graphene.String)


class BookAuthorQueryType(DjangoObjectType):
    class Meta:
        model = BookAuthor
        fields = ['author']


class BookInputType(graphene.InputObjectType):
    author = graphene.Field(BookAuthorInputType, required=True)
    ISBN = graphene.Argument(graphene.String, required=True)
    title = graphene.Argument(graphene.String, required=True)
    tags = graphene.Argument(graphene.List(BookTagENUM))
    description = graphene.Argument(graphene.String)


class BookQueryType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"

    authors = graphene.List(BookAuthorQueryType)
    def resolve_authors(root, info):
        return root.authors.all()


class BookListType(graphene.ObjectType):
    data = graphene.List(BookQueryType)
    page_count = graphene.Int()
    count = graphene.Int()


class BookFilterType(graphene.InputObjectType):
    is_active = graphene.Boolean()
    tags = graphene.Argument(graphene.List(BookTagENUM))


class BookEditInputType(graphene.InputObjectType):
    pk = graphene.Argument(graphene.ID, required=True)
    ISBN = graphene.Argument(graphene.String)
    title = graphene.Argument(graphene.String)
    description = graphene.Argument(graphene.String)
    tags = graphene.Argument(graphene.List(BookTagENUM))
    is_active = graphene.Argument(graphene.Boolean)
