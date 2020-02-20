from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from graphql import execute, parse

from graphql_utilities.decorators import run_only_once
from tests.helpers import assert_no_errors
from tests.schema import schema

settings.configure(name="TEST")


def describe_run_only_once():
    query = '{ field_1_str field_2_int field_3_obj { field_3_obj_sub_1 { xxx } } }'

    def test_run_only_once():
        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        runs = []
        middleware = (OneShotMiddleware(),)

        result = execute(schema=schema, document=parse(query),
                         middleware=middleware, context_value={})
        assert_no_errors(result)
        assert len(runs) == 1, "middleware should run only once"

    def test_run_only_once_doesnt_affect_other_middleware():
        runs = []

        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        class FieldMiddleware:
            def resolve(self, next_, *args, **kwargs):
                runs.append("FieldMiddleware")
                return next_(*args, **kwargs)

        result = execute(schema=schema, document=parse(query),
                         middleware=(FieldMiddleware(), OneShotMiddleware()),
                         context_value={})
        assert_no_errors(result)
        assert len(runs) == 5
        assert runs.count("OneShotMiddleware") == 1
        assert runs.count("FieldMiddleware") == 4

    def test_middleware_run_on_multiple_requests():
        runs = []

        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        middleware = (OneShotMiddleware(),)
        [execute(schema=schema, document=parse(query), middleware=middleware, context_value={}) for _ in (0, 1)]
        assert len(runs) == 2, "middleware should run twice for 2 requests"

    def test_middleware_with_graphene_context_values():
        runs = []

        class Context(object):
            # This class is taken from Graphene source code
            def __init__(self, **params):
                for key, value in params.items():
                    setattr(self, key, value)

        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        middleware = (OneShotMiddleware(),)
        [execute(schema=schema, document=parse(query), middleware=middleware, context_value=Context()) for _ in (0, 1)]
        assert len(runs) == 2, "middleware should run twice for 2 requests"

    def test_middleware_with_wsgi_request_context_values():
        runs = []

        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        middleware = (OneShotMiddleware(),)
        [execute(schema=schema, document=parse(query), middleware=middleware,
                 context_value=_get_fake_wsgi_request_obj()) for _ in (0, 1)]
        assert len(runs) == 2, "middleware should run twice for 2 requests"

    def test_multiple_one_shot_middleware():
        runs = []
        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        class AnotherOneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("AnotherOneShotMiddleware")
                return next_(*args, **kwargs)

        middleware = (OneShotMiddleware(), AnotherOneShotMiddleware())
        execute(schema=schema, document=parse(query), middleware=middleware,
                context_value={})
        assert len(runs) == 2, "both middleware should have run"
        assert "OneShotMiddleware" in runs
        assert "AnotherOneShotMiddleware" in runs

    def _get_fake_wsgi_request_obj():
        return WSGIRequest({
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/graphql',
            'wsgi.input': ""})
