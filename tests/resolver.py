from tests.fixtures import get_posts


class PostRootResolver:
    def posts(self, info, pagination, *args, **kwargs):
        # Pagination is meant to be working here :)
        # It's only for cost analysis
        post_count = pagination.get('first', 10)
        return [p for p in get_posts(post_count=post_count)]

    def post(self, *args, **kwargs):
        return list(get_posts(1))[0]

