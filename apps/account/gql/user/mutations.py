import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from helpers import http_code
from helpers.generic_types import ResponseBase
from apps.account.gql.user.types import UserEditInputType
from apps.account.models import User
from apps.account.models import Author
class UserEdit(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(UserEditInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        User.clean_fields(**data)

        if data.get("password"):
            user.set_password(data.pop("password"))

        if not data.get("is_author"):
            User.objects.filter(phone_number=user).update(**data)
        elif not user.is_author:
            author = Author(user=user, first_name="no-firstname", last_name="no-lastname")
            author.clean()
            author.save()

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Changed successfully!"),
        )
