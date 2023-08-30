import graphql_jwt
from apps.account.gql.authentication.mutations import CreateLogin
from apps.account.gql.authentication.mutations import Logout
from apps.account.gql.user.mutations import UserEdit
from apps.account.gql.author.mutations import AuthorEdit
from apps.account.gql.relation.mutations import UserFollow

from apps.account.gql.user.queries import UserList
from apps.account.gql.user.queries import UserDetail
from apps.account.gql.author.queries import AuthorList
from apps.account.gql.author.queries import AuthorDetail
from apps.account.gql.relation.queries import UserFollowerList
from apps.account.gql.relation.queries import UserFollowingList

class Query(UserList, UserDetail, AuthorList, AuthorDetail, UserFollowerList, UserFollowingList):
    pass


class Mutation:

    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = CreateLogin.Field()
    logout = Logout.Field()
    user_edit = UserEdit.Field()
    author_edit = AuthorEdit.Field()
    user_follow = UserFollow.Field()
