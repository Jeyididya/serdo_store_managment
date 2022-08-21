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
    # user = graphene.List(userType,username=graphene.String())
    users=graphene.List(userType)
    me = graphene.Field(userType)
    class Arguments:
        username = graphene.String(required=True)

    def resolve_users(self, info):
        return user.objects.all()
    # def resolve_user(self, info, username):
    #     return user.objects.filter(username=username)

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
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()




# schemaa = graphene.Schema(query=userQuery)

# result=schemaa.execute(

#     """
#    query{
#     users{
#         username
#         email
#         isActive
#       }
  
    
# }
    
#     """

# )

# print("-->>",result.data)
