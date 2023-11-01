import graphene
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from apps.account.gql.relation.types import FollowInputType
from apps.account.models import Relation
from apps.account.models import User
from helpers import http_code
from helpers.generic_types import ResponseBase


class UserFollow(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(
            FollowInputType,
            description="Input data for user following.",
        )

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):
        """
        Mutate to follow a user.

        Args:
            data (FollowInputType): Input data for following a user.

        Returns:
            ResponseBase: Response indicating the success or failure of the following operation.
        """

        user = info.context.user
        followed_user = User.objects.filter(Q(id=data.get("id")) | Q(phone_number=data.get("phone_number"))).first()

        rel = Relation(follower=user, following=followed_user)
        rel.save()

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Followed successfully!"),
        )
