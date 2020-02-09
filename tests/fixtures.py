import uuid


def get_posts(post_count):
    post_id = 1
    for n in range(post_count):
        yield {
            "author": None,
            "postId": uuid.uuid4(),
            "title": f"Random Post #{post_id}",
            "text": "Lorem ipsum dolor sit amet.",
            "publishedAt": None,
            "isPublic": False,
            "createdAt": "2020-02-08T08:31:53+00:00",
            "updatedAt": "2020-02-08T08:54:53+00:00"
        }
        post_id += 1
