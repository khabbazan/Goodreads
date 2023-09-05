import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from apps.account.gql.author.types import AuthorEditInputType
from apps.account.models import Author
from helpers import http_code
from helpers.generic_types import ResponseBase
from helpers.cache.decorators import expire_cache_keys

class AuthorEdit(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(
            AuthorEditInputType,
            description="Input data for author editing.",
        )

    Output = ResponseBase

    @expire_cache_keys(["author.list"])
    @login_required
    def mutate(self, info, data):
        """
        Mutate to edit an author's information.

        Args:
            data (AuthorEditInputType): Input data for editing author information.

        Returns:
            ResponseBase: Response indicating the success or failure of the editing operation.
        """

        user = info.context.user
        Author.clean_fields(**data)

        Author.objects.filter(user__phone_number=user).update(**data)

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Changed successfully!"),
        )
