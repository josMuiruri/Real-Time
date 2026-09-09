import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# structural shape
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'company')

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, password, email):
        if CustomUser.objects.filter(username=username).exists():
            raise Exception('Username taken.')
        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        return RegisterUser(user=user)

class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()