import graphene
class UserInputType(graphene.InputObjectType):
    phone_number = graphene.Argument(graphene.String, required=True)
    password = graphene.Argument(graphene.String, required=True)
