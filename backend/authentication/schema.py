from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from .models import *

class userType(DjangoObjectType):
    class Meta:
        model = user
        # filter_fields = ['username']
        # interfaces = (graphene.relay.Node,)

class userQuery(graphene.ObjectType):
    user = graphene.List(userType)
    me = graphene.Field(userType)
    def resolve_user(self, info):
        return user.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

class createUser(graphene.Mutation):
    user = graphene.Field(userType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()

    

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return createUser(user=user)

class authMutation(graphene.ObjectType):
    create_user = createUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()



