import graphene
from graphql_jwt.decorators import login_required

from apps.book.gql.shelf.types import UserShelfListQueryType

class UserShelfList(graphene.ObjectType):

    user_shelf_list = graphene.List(
        UserShelfListQueryType,
        description="Get the list of shelves associated with the authenticated user.",
    )

    @login_required
    def resolve_user_shelf_list(self, info):
        """
        Resolve the user_shelf_list field to retrieve the list of shelves associated with the authenticated user.

        Args:
            info (GraphQLResolveInfo): The GraphQL resolve info.

        Returns:
            List[UserShelfListQueryType]: A list of shelves associated with the user.
        """
        user = info.context.user

        return user.bookshelf_users.all()
