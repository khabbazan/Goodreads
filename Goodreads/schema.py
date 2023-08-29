import graphene

from apps.account.gql.schema import Mutation as AccountMutation
from apps.account.gql.schema import Query as AccountQuery

class Query(
    AccountQuery,

):
    pass


class Mutation(graphene.ObjectType, AccountMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
