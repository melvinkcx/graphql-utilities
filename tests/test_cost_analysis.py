from graphql import graphql_sync

from tests.helpers import assert_no_errors
from tests.resolver import PostRootResolver
from tests.schema import post_schema


def describe_cost_analysis():
    def get_query(first=10):
        return """
            query {
                posts(pagination: {first: """ + str(first) + """}) {
                    postId
                }
            }
        """

    def test_schema():
        result = graphql_sync(post_schema, get_query(5), PostRootResolver())
        posts = result.data.get("posts")
        assert_no_errors(result)
        assert len(posts) == 5
