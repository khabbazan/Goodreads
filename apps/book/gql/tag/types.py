import graphene
from graphene_django import DjangoObjectType

from apps.book.models import Tag

# Define a query object type for tags.
class TagListType(DjangoObjectType):
    """
    Query type for retrieving tag data.
    """
    class Meta:
        model = Tag
        fields = ("id",)

    name = graphene.String(description="Name of the tag.")
    def resolve_name(root, info):
        """
        Resolve the name of the tag.
        """
        return root.name

    display_name = graphene.String(description="Display name of the tag.")
    def resolve_display_name(root, info):
        """
        Resolve the display name of the tag.
        """
        return root.get_name_display()
