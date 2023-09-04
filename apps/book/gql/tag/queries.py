import graphene
from apps.book.gql.tag.types import TagListType
from apps.book.models import Tag


class TagList(graphene.ObjectType):
    tag_list = graphene.List(TagListType, search=graphene.String())

    def resolve_tag_list(self, info, **kwargs):
        search = kwargs.get("search", "")
        if search:
            return Tag.objects.search(search)
        return Tag.objects.all()
