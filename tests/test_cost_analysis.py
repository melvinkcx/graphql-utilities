from graphql import graphql_sync

from graphql_utilities import ExtendedExecutionContext
from tests.helpers import assert_no_errors, assert_has_data
from tests.resolver import PostRootResolver
from tests.schema import post_schema


def describe_cost_analysis():
    resolver = PostRootResolver()

    def get_posts_query(first=10):
        return """
            query {
                posts(pagination: {first: """ + str(first) + """}) {
                    postId
                }
            }
        """

    def get_single_post_query():
        return """
            query {
                post(id: "XXXXXXXXXXXXXX") {
                    postId
                    title
                }
            }
        """

    def test_schema_get_posts():
        result = graphql_sync(post_schema, get_posts_query(5), resolver)
        posts = result.data.get("posts")
        assert_no_errors(result)
        assert len(posts) == 5

    def test_schema_get_single_post():
        result = graphql_sync(post_schema, get_single_post_query(), resolver)
        assert_no_errors(result)
        assert_has_data(result)

    def test_simple_cost():
        result = graphql_sync(post_schema, get_single_post_query(), resolver,
                              context_value={"cost_analysis": {
                                  "max_complexity": 100
                              }},
                              execution_context_class=ExtendedExecutionContext)
        breakpoint()
