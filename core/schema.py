import graphene
import management.schema

class Query(management.schema.Query, graphene.ObjectType):
    pass

class Mutation(management.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)