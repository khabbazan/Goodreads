import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from helpers import http_code
from helpers.generic_types import ResponseBase
from apps.account.gql.user.types import UserEditInputType
from apps.account.models import User
class UserEdit(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(UserEditInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        user.clean_fields(**data)
        if data.get("password"):
            user.set_password(data.pop("password"))

        User.objects.filter(phone_number=user).update(**data)


        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Changed successfully!"),
        )
