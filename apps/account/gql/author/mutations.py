import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from helpers import http_code
from helpers.generic_types import ResponseBase
from apps.account.gql.author.types import AuthorEditInputType
from apps.account.models import Author

class AuthorEdit(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(AuthorEditInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        Author.clean_fields(**data)

        Author.objects.filter(user__phone_number=user).update(**data)

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Changed successfully!"),
        )
