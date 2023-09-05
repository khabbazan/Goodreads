import graphene
from django.db import transaction
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token

from helpers import http_code
from helpers.generic_types import ResponseUnion
from helpers.generic_types import ResponseBase
from helpers.generic_types import ResponseWithToken
from apps.account.models import User
from apps.account.gql.authentication.types import UserInputType

class CreateLogin(graphene.Mutation):
    class Arguments:
        user_input = graphene.Argument(
            UserInputType,
            description="Input data for user login or registration.",
            default_value={},
        )

    Output = ResponseUnion

    def mutate(self, info, user_input):
        """
        Mutate to create a new user or log in an existing user.

        Args:
            user_input (UserInputType): Input data for user login or registration.

        Returns:
            ResponseUnion: Response indicating the success or failure of the login/registration operation.
        """
        existence_state = User.objects.filter(phone_number=user_input["phone_number"]).exists()

        if existence_state:
            user = authenticate(username=user_input["phone_number"], password=user_input["password"])
        else:
            with transaction.atomic():
                user = User.objects.create_user(
                    password=user_input.pop("password"),
                    phone_number=user_input.pop("phone_number"),
                    **user_input,
                )

        if user:
            return ResponseWithToken(
                status=http_code.HTTP_200_OK,
                status_code=http_code.HTTP_200_OK_CODE,
                message=_("Login Successfully!"),
                token=get_token(user),
                refresh_token=create_refresh_token(user),
                metadata={k: v for k, v in vars(user).items() if k in ["id", "phone_number"]},
            )
        else:
            return ResponseBase(
                status=http_code.HTTP_401_UNAUTHORIZED,
                status_code=http_code.HTTP_401_UNAUTHORIZED_CODE,
                message=_("Login Failed!"),
            )

class Logout(graphene.Mutation):

    Output = ResponseBase

    @login_required
    def mutate(self, info, **kwargs):
        """
        Mutate to log out the current user by deleting their refresh tokens.

        Returns:
            ResponseBase: Response indicating the success of the logout operation.
        """
        deleted, __ = info.context.user.refresh_tokens.all().delete()

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_(f"Successfully deleted {deleted} token(s)."),
        )
