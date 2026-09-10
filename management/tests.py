from graphene_django.utils.testing import GraphQLTestCase
from core.schema import schema

# Create your tests here.
class GraphQLSecurityTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    GRAPHQL_URL = '/graphql'

    def test_my_projects_query_is_blocked_for_anonymous_users(self):
        '''verify security middleware protects data queries'''
        response = self.query(
            '''
            query {
                myProjects {
                    name
                }
            }
            '''
        )
        self.assertResponseHasErrors(response)