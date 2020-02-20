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

    @wraps(resolve_func)
    def wrapper(self, next, root, info, *args, **kwargs):
        has_context = info.context is not None
        decorator_name = "__{}_run__".format(self.__class__.__name__)

        if has_context:
            if isinstance(info.context, dict) and not info.context.get(decorator_name, False):
                info.context[decorator_name] = True
                return resolve_func(self, next, root, info, *args, **kwargs)
            elif not isinstance(info.context, dict) and not getattr(info.context, decorator_name, False):
                # Graphene: it could be a Context or WSGIRequest object
                setattr(info.context, decorator_name, True)
                return resolve_func(self, next, root, info, *args, **kwargs)

        # No context, run_only_once will not work
        return next(root, info, *args, **kwargs)

    return wrapper
