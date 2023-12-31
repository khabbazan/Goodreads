import graphene


class UserInputType(graphene.InputObjectType):
    """
    Input type for user data during registration or login.
    """

    phone_number = graphene.Argument(graphene.String, required=True, description="User's phone number for registration or login.")
    email = graphene.Argument(graphene.String, required=True, description="User's email for registration or login.")
    password = graphene.Argument(graphene.String, required=True, description="User's password for authentication.")
