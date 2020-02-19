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

        if has_context:
            if isinstance(info.context, dict) and not info.context.get("__middleware_ran", False):
                info.context["__middleware_ran"] = True
                return resolve_func(self, next, root, info, *args, **kwargs)
            elif not isinstance(info.context, dict) and not getattr(info.context, "__middleware_ran", False):
                # Graphene: it could be a Context or WSGIRequest object
                setattr(info.context, "__middleware_ran", True)
                return resolve_func(self, next, root, info, *args, **kwargs)

        # No context, run_only_once will not work
        return next(root, info, *args, **kwargs)

    return wrapper
