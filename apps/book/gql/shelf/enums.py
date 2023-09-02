import graphene

from apps.book.models import Shelf

ShelfENUM = graphene.Enum("shelf_name", Shelf.ShelfName)
