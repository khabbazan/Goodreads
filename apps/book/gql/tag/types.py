import graphene
from graphene_django import DjangoObjectType

from apps.book.models import Tag

class TagListType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id",)

    name = graphene.String()

    def resolve_name(root, info):
        return root.name

    display_name = graphene.String()

    def resolve_display_name(root, info):
        return root.get_name_display()
