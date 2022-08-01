import inventory.schema_relay as inventory_schema
import authentication.schema as authentication_schema
import sales.schema as sales_schema
import graphql_jwt
import graphene

class Query(inventory_schema.inventoryQuery,authentication_schema.userQuery,sales_schema.query ,graphene.ObjectType):
    pass


class Mutation(authentication_schema.authMutation,inventory_schema.inventoryMutations,sales_schema.mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
