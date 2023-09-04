import graphene

from apps.book.models import Tag

BookTagENUM = graphene.Enum("book_tag", Tag.TAG)
