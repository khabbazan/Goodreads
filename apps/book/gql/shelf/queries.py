import graphene
from graphql_jwt.decorators import login_required

from apps.book.gql.shelf.types import UserShelfListQueryType

class UserShelfList(graphene.ObjectType):

    user_shelf_list = graphene.List(
        UserShelfListQueryType,
    )

    @login_required
    def resolve_user_shelf_list(self, info):

        user = info.context.user

        return user.bookshelf_users.all()
