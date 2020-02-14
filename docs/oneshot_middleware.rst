.. _oneshot_middleware:

Operation-level/One-shot Middleware
====================================

The problem of using middleware in `graphql-core` in Python is it run at field-level.
If you use a middleware to perform authentication,
you probably don't want the authentication logic run when the engine tries to resolve every single field.s

.. code-block:: python

    from graphql_utilities.decorators import run_only_once

    class AuthMiddleware:
        @run_only_once
        def resolve(self, next_, root, info, *args, **kwargs):
            # middleware logic
            return next_(root, info, *args, **kwargs)
