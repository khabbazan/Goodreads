import graphene

from apps.account.gql.schema import Mutation as AccountMutation
from apps.account.gql.schema import Query as AccountQuery

import graphene

from apps.account.gql.schema import Mutation as AccountMutation
from apps.account.gql.schema import Query as AccountQuery

# class Query(
#     AccountQuery,
#
# ):
#     pass

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")

class Mutation(graphene.ObjectType, AccountMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
