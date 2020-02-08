from graphql import parse

from tests.fixtures import posts_data


class PostRootResolver:
    def posts(self, *args, **kwargs):
        return posts_data


posts_query = parse("""
    {
        posts(input: {isPublic: true, isPublished: true}) {
            postId
        }
    }
""")
