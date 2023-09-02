import graphene

from apps.account.models import User

UserGenderENUM = graphene.Enum("user_gender", User.GENDER)
