import graphene
from django.utils.translation import gettext_lazy as _
from graphql_jwt.decorators import login_required

from apps.account.gql.user.types import UserEditInputType
from apps.account.models import User
from apps.account.models import Author
from apps.extension.models import Image
from helpers import http_code
from helpers.generic_types import ResponseBase
from helpers.cache.decorators import expire_cache_keys

class UserEdit(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(UserEditInputType)

    Output = ResponseBase

    @expire_cache_keys(["user.list"])
    @login_required
    def mutate(self, info, data):

        user = info.context.user
        data = User.clean_fields(**data)

        if data.get("password"):
            user.set_password(data.pop("password"))

        if data.get("gender"):
            data["gender"] = getattr(data["gender"], "name", data.get("gender"))

        if data.get("base64_image"):
            image_content = Image.base64_to_image(data.pop("base64_image"))
            user.avatar = image_content
            user.save()
        elif data.get("base64_image") == "":
            user.avatar.delete()

        if data.get("is_author") and not user.is_author:
            author = Author(user=user, first_name="no-firstname", last_name="no-lastname")
            author.clean()
            author.save()

        User.objects.filter(phone_number=user).update(**data)

        return ResponseBase(
            status=http_code.HTTP_200_OK,
            status_code=http_code.HTTP_200_OK_CODE,
            message=_("Changed successfully!"),
        )
