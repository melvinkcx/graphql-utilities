from tests.fixtures import get_posts


class PostRootResolver:
    def posts(self, info, first, *args, **kwargs):
        # Pagination isn't meant to be working here :)
        # It's only for cost analysis
        return get_posts(post_count=first)

    def post(self, *args, **kwargs):
        return list(get_posts(1))[0]

