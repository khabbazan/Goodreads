import graphene

# Define an input object type for user input.
class UserInputType(graphene.InputObjectType):
    """
    Input type for user data during registration or login.
    """
    phone_number = graphene.Argument(graphene.String, required=True, description="User's phone number for registration or login.")
    password = graphene.Argument(graphene.String, required=True, description="User's password for authentication.")
