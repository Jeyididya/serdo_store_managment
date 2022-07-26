import inventory.schema_relay as inventory_schema
import authentication.schema as authentication_schema
import sales.schema as sales_schema
import purchase.schema as purchase_schema
import graphene

class Query(inventory_schema.inventoryQuery,authentication_schema.userQuery,sales_schema.query,purchase_schema.Query ,graphene.ObjectType):
    pass


class Mutation(authentication_schema.authMutation,inventory_schema.inventoryMutations,sales_schema.mutation,purchase_schema.mutations,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
