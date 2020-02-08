from typing import List, Any

from graphql import graphql_sync

from graphql_utilities.decorators import run_only_once
from tests.helpers import assert_no_errors
from tests.schema import schema


def describe_run_only_once():
    def test_run_only_once():
        runs: List[Any] = []

        class Middleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append(True)
                return next_(*args, **kwargs)

        query = '{ field_1_str field_2_int field_3_obj { field_3_obj_sub_1 { xxx } } }'

        result = graphql_sync(schema=schema, source=query, middleware=[Middleware()])
        assert_no_errors(result)
        assert len(runs) == 1, "middleware should run only once"

    def test_run_only_once_doesnt_affect_other_middlewares():
        runs: List[Any] = []

        class FieldMiddleware:
            def resolve(self, next_, *args, **kwargs):
                runs.append("FieldMiddleware")
                return next_(*args, **kwargs)

        class OneShotMiddleware:
            @run_only_once
            def resolve(self, next_, *args, **kwargs):
                runs.append("OneShotMiddleware")
                return next_(*args, **kwargs)

        query = '{ field_1_str field_2_int field_3_obj { field_3_obj_sub_1 { xxx } } }'

        result = graphql_sync(schema=schema, source=query, middleware=[FieldMiddleware(), OneShotMiddleware()])
        assert_no_errors(result)
        assert len(runs) == 5
        assert runs.count("OneShotMiddleware") == 1
        assert runs.count("FieldMiddleware") == 4
