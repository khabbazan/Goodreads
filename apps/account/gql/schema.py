import graphql_jwt
from apps.account.gql.authentication.mutations import CreateLogin
from apps.account.gql.authentication.mutations import Logout
from apps.account.gql.user.mutations import UserEdit

from apps.account.gql.user.queries import UserList
from apps.account.gql.user.queries import UserDetail

class Query(UserList, UserDetail):
    pass


class Mutation:

    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = CreateLogin.Field()
    logout = Logout.Field()
    user_edit = UserEdit.Field()
