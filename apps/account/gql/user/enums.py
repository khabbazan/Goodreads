import graphene

from apps.account.choices import GENDER

UserGenderENUM = graphene.Enum("user_gender", GENDER)
