import graphene
from apps.book.gql.tag.types import TagListType
from apps.book.models import Tag

class TagList(graphene.ObjectType):
    tag_list = graphene.List(
        TagListType,
        search=graphene.String(description="Search for tags based on a keyword."),
        description="Get a list of tags.",
    )

    def resolve_tag_list(self, info, **kwargs):
        """
        Resolve the tag_list field to retrieve a list of tags.

        Args:
            info (GraphQLResolveInfo): The GraphQL resolve info.
            search (str, optional): Search keyword for tags. Defaults to an empty string.

        Returns:
            List[TagListType]: A list of tags.
        """
        search = kwargs.get("search", "")
        if search:
            return Tag.objects.search(search)
        return Tag.objects.all()
