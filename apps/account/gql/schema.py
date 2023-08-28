import graphql_jwt
from apps.account.gql.authentication.mutations import CreateLogin
from apps.account.gql.authentication.mutations import Logout


class Query:
    pass


class Mutation:

    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = CreateLogin.Field()
    logout = Logout.Field()
