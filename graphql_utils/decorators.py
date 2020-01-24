from typing import NamedTuple


def run_only_once(resolve_func):
    """
    Make sure middleware is run only once,
    this is done by setting a flag in the `context` of `ResolverInfo`

    Example:
        class AuthenticationMiddleware:
            @run_only_once
            def resolve(self, next, root, info, *args, **kwargs):
                pass
    
    """
    from functools import wraps

    # Use closure to keep track of middleware
    middleware_run = dict()

    @wraps(resolve_func)
    def wrapper(self, next, root, info, *args, **kwargs):
        middleware_name = self.__class__.__name__
        if not middleware_run.get(middleware_name):
            middleware_run[middleware_name] = True
            return resolve_func(self, next, root, info, *args, **kwargs)

        return next(root, info, *args, **kwargs)

    return wrapper
