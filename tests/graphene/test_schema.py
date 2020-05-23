import graphene
import pytest

from graphql_utilities.execution import ExtendedExecutionContext


@pytest.mark.skip(reason="TODO")
def describe_cost_analysis_with_graphene_schema():
    """
    Objectives:
    - To find a way to define cost of queries in Graphene schema
    - To ensure cost analysis works with schema defined with Graphene
    """

    def test_define_object_complexity():
        """
        type Post @cost(complexity: 5) {
            postId: ID!
            title: String
        }
        """
        pass

    def test_define_field_complexity():
        """
        type Post {
            postId: ID!
            title: String
            lastSnapshot: String @cost(complexity: 8)
        }
        """

        class Post(graphene.ObjectType):
            post_id: graphene.ID(required=True)
            title: graphene.String()
            last_snapshot: graphene.String()

        class Query(graphene.ObjectType):
            post = graphene.Field(Post)

            def resolve_post(self, *args, **kwargs):
                return {"postId": "1a34", "title": "This is a title", "last_snapshot": "This is a value"}

        graphene_schema = graphene.Schema(query=Query)
        query = """
            {
                post 
            }
        """
        graphene_schema.execute(query, execution_context_class=ExtendedExecutionContext)

    def test_define_object_and_field_complexity():
        """
        type Post @cost(complexity: 5) {
            postId: ID!
            title: String
            lastSnapshot: String @cost(complexity: 8)
        }
        """
        pass
