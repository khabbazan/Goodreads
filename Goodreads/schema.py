import graphene

from apps.account.gql.schema import Mutation as AccountMutation
from apps.account.gql.schema import Query as AccountQuery
from apps.book.gql.schema import Mutation as BookMutation
from apps.book.gql.schema import Query as BookQuery


class Query(
    AccountQuery,
    BookQuery,
):
    pass


class Mutation(graphene.ObjectType, AccountMutation, BookMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
