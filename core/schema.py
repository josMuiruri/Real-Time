import graphene
import management.schema

class Query(management.schema.Query, graphene.ObjectType):
    pass

class Mutation(management.schema.Mutation, graphene.ObjectType):
    create_project = management.schema.CreateProject.Field()

class Subscription(management.schema.Subscription, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)