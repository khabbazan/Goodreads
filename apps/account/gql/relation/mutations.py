import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required
from django.db.models import Q

from helpers import http_code
from helpers.generic_types import ResponseBase
from apps.account.gql.relation.types import FollowInputType
from apps.account.models import Relation
from apps.account.models import User

class UserFollow(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(FollowInputType)

    Output = ResponseBase

    @login_required
    def mutate(self, info, data):

        user = info.context.user
        followed_user = User.objects.filter(
            Q(id=data.get("id")) | Q(phone_number=data.get("phone_number"))
        ).first()

        rel = Relation(follower=user, following=followed_user)
        rel.save()

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("followed successfully!"),
        )
